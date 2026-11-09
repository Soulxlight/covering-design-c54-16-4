// wls2: weighted local search for covering designs with incremental move scores.
//
// Same search as wls128 (t-set weighting + tabu + shrink mode), but moves are scored in O(C(k,t-1)) per
// candidate block instead of O((k-t+1) * C(k-1,t-1)):
//   brk[i][x] = total weight of t-sets S with cov[S]==1, S inside block i, x in S  (maintained incrementally;
//               the unique owner of a cov==1 set is recovered from sid[S] = sum of the ids of covering blocks)
//   make(i, xin, xout) = M - m1[xout], where one pass over the (t-1)-subsets R of block i accumulates
//               M = sum of w[R+xin] over uncovered R+xin, and m1[p] = the part of M whose R contains p.
// Weights only grow on uncovered t-sets (cov==0), which never appear in brk, so brk stays exact.
//
// Usage: wls2 v k t b seconds seed [init_file|-] [tenure=7] [noise=0.05] [targetB]
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <cstring>
#include <vector>
#include <random>
#include <chrono>
#include <algorithm>
using namespace std;
typedef uint64_t u64;
typedef uint64_t M;
static inline int ctz128(M x) { return __builtin_ctzll(x); }
static inline int pc128(M x) { return __builtin_popcountll(x); }
#define BIT(p) (((M)1) << (p))

int v, k, t, b;
u64 Cb[130][20];
inline u64 binom(int n, int r) { return (r < 0 || n < r || n < 0) ? 0 : Cb[n][r]; }

vector<uint16_t> cov;
vector<uint32_t> sid;   // sum of ids of blocks covering S
vector<uint32_t> w;
vector<u64> unc; vector<int64_t> upos;
vector<M> bm;
vector<int64_t> brk;    // brk[i*128 + x]
vector<int> tabuUntil;  // tabuUntil[i*128 + x]
vector<uint32_t> rank4;
vector<M> target_mask; // fixed rank-to-mask table for sparse uncovered scoring
size_t triple_count;
long step = 0;

inline void add_unc(u64 r) { upos[r] = unc.size(); unc.push_back(r); }
inline void rem_unc(u64 r) { int64_t p = upos[r]; u64 l = unc.back(); unc[p] = l; upos[l] = p; unc.pop_back(); upos[r] = -1; }

inline u64 rank_pts(const int* p, int n) { u64 r = 0; for (int i = 0; i < n; ++i) r += binom(p[i], i + 1); return r; }  // p ascending
inline M unrank(u64 r) {
    M m = 0;
    for (int i = t; i >= 1; --i) { int c = i - 1; while (binom(c + 1, i) <= r) ++c; m |= BIT(c); r -= binom(c, i); }
    return m;
}
inline int pts_of(M m, int* p) { int n = 0; for (; m; m &= m - 1) p[n++] = ctz128(m); return n; }

// enumerate r-subsets of the sorted point list P (size n); f(idx array)
template <class F> inline void subsets(int n, int r, F f) {
    int idx[20]; for (int i = 0; i < r; ++i) idx[i] = i;
    if (r > n) return;
    while (true) {
        f(idx);
        int i = r - 1; while (i >= 0 && idx[i] == n - r + i) --i;
        if (i < 0) return;
        ++idx[i]; for (int l = i + 1; l < r; ++l) idx[l] = idx[l - 1] + 1;
    }
}

// t-sets of block mask B that contain point x: call f(rank, sorted points of S)
template <class F> inline void each_with(M B, int x, F f) {
    int P[128]; int n = pts_of(B & ~BIT(x), P);
    if (t == 4) {
        size_t base = x * triple_count;
        for (int a = 0; a < n - 2; ++a)
            for (int bb = a + 1; bb < n - 1; ++bb) {
                size_t ab = base + Cb[P[a]][1] + Cb[P[bb]][2];
                for (int c = bb + 1; c < n; ++c) {
                    int S[4] = {x, P[a], P[bb], P[c]};
                    f(rank4[ab + Cb[P[c]][3]], S);
                }
            }
        return;
    }
    subsets(n, t - 1, [&](int* idx) {
        int S[20]; int m = 0; bool placed = false;
        for (int i = 0; i < t - 1; ++i) { int q = P[idx[i]]; if (!placed && x < q) { S[m++] = x; placed = true; } S[m++] = q; }
        if (!placed) S[m++] = x;
        f(rank_pts(S, t), S);
    });
}
template <class F> inline void each_all(M B, F f) {
    int P[128]; int n = pts_of(B, P);
    if (t == 4) {
        for (int a = 0; a < n - 3; ++a)
            for (int bb = a + 1; bb < n - 2; ++bb)
                for (int c = bb + 1; c < n - 1; ++c) {
                    u64 base = Cb[P[a]][1] + Cb[P[bb]][2] + Cb[P[c]][3];
                    for (int d = c + 1; d < n; ++d) {
                        int S[4] = {P[a], P[bb], P[c], P[d]};
                        f(base + Cb[P[d]][4], S);
                    }
                }
        return;
    }
    subsets(n, t, [&](int* idx) { int S[20]; for (int i = 0; i < t; ++i) S[i] = P[idx[i]]; f(rank_pts(S, t), S); });
}

inline void brk_add(int blk, const int* S, int64_t d) { int64_t* row = &brk[(size_t)blk * 128]; for (int i = 0; i < t; ++i) row[S[i]] += d; }

// t-set S (rank r) gains block blk
inline void cover_inc(u64 r, const int* S, int blk) {
    uint16_t c = cov[r]++;
    if (c == 0) { rem_unc(r); brk_add(blk, S, w[r]); }
    else if (c == 1) brk_add(sid[r], S, -(int64_t)w[r]);
    sid[r] += blk;
}
// t-set S (rank r) loses block blk
inline void cover_dec(u64 r, const int* S, int blk) {
    sid[r] -= blk;
    uint16_t c = --cov[r];
    if (c == 0) { add_unc(r); brk_add(blk, S, -(int64_t)w[r]); }
    else if (c == 1) brk_add(sid[r], S, w[r]);
}

void save(const char* fn) {
    char temp[1024]; snprintf(temp, sizeof(temp), "%s.tmp", fn);
    FILE* f = fopen(temp, "w"); if (!f) { perror(temp); exit(2); }
    for (M m : bm) { int c = 0; for (int p = 0; p < v; ++p) if ((m >> p) & 1) fprintf(f, "%d%c", p + 1, ++c < k ? ' ' : '\n'); }
    if (fclose(f) != 0 || rename(temp, fn) != 0) { perror(fn); exit(2); }
}

#include "background_move.hpp"

bool noWeight = false;
int main(int argc, char** argv) {
    noWeight = getenv("NOWEIGHT") != nullptr;
    if (argc < 7) { fprintf(stderr, "usage: wls2 v k t b seconds seed [init|-] [tenure] [noise] [targetB]\n"); return 1; }
    v = atoi(argv[1]); k = atoi(argv[2]); t = atoi(argv[3]); b = atoi(argv[4]);
    if (v > 64) { fprintf(stderr, "64-bit build requires v<=64\n"); return 2; }
    double secs = atof(argv[5]); unsigned seed = atoi(argv[6]);
    const char* init = (argc > 7 && argv[7][0] != '-') ? argv[7] : nullptr;
    int tenure = argc > 8 ? atoi(argv[8]) : 7;
    double noise = argc > 9 ? atof(argv[9]) : 0.05;
    int targetB = argc > 10 ? atoi(argv[10]) : b;
    for (int n = 0; n < 130; ++n) { Cb[n][0] = 1; for (int r = 1; r < 20; ++r) Cb[n][r] = n ? Cb[n - 1][r - 1] + Cb[n - 1][r] : 0; }
    u64 NT = binom(v, t);
    target_mask.resize(NT);
    for (u64 r = 0; r < NT; ++r) target_mask[r] = unrank(r);
    if (t == 4) {
        triple_count = binom(v, 3);
        rank4.resize((size_t)v * triple_count);
        for (int x = 0; x < v; ++x)
            for (int a = 0; a < v - 2; ++a)
                for (int bb = a + 1; bb < v - 1; ++bb)
                    for (int c = bb + 1; c < v; ++c) {
                        int P[4] = {x, a, bb, c};
                        if (x == a || x == bb || x == c) continue;
                        sort(P, P + 4);
                        rank4[x * triple_count + Cb[a][1] + Cb[bb][2] + Cb[c][3]] = rank_pts(P, 4);
                    }
    }
    cov.assign(NT, 0); sid.assign(NT, 0); w.assign(NT, 1); upos.assign(NT, -1);
    mt19937_64 rng(seed);
    bm.assign(b, 0);
    int loaded = 0;
    if (init) {
        FILE* f = fopen(init, "r");
        for (int i = 0; i < b && f; ++i) {
            M m = 0; int cnt = 0;
            for (int j = 0; j < k; ++j) { int p; if (fscanf(f, "%d", &p) == 1) { m |= BIT(p - 1); ++cnt; } }
            if (cnt == k) { bm[i] = m; ++loaded; } else break;
        }
        if (f) fclose(f);
    }
    for (int i = loaded; i < b; ++i) {
        vector<int> pts(v); for (int p = 0; p < v; ++p) pts[p] = p; shuffle(pts.begin(), pts.end(), rng);
        M m = 0; for (int j = 0; j < k; ++j) m |= BIT(pts[j]); bm[i] = m;
    }
    brk.assign((size_t)b * 128, 0); tabuUntil.assign((size_t)b * 128, 0);
    for (u64 r = 0; r < NT; ++r) add_unc(r);
    for (int i = 0; i < b; ++i) each_all(bm[i], [&](u64 r, const int* S) { cover_inc(r, S, i); });
    long best = unc.size();
    fprintf(stderr, "init: loaded %d blocks, uncovered %ld\n", loaded, best);
    auto start = chrono::steady_clock::now();
    double nextReport = 10.0;
    const char* partial = getenv("SAVE_PARTIAL");
    if (partial) save(partial);
    long maxSteps = getenv("MAX_STEPS") ? atol(getenv("MAX_STEPS")) : 0;
    uniform_real_distribution<double> U01(0, 1);
    int bestFull = -1;
    int backgroundEvery=getenv("BACKGROUND_EVERY")?atoi(getenv("BACKGROUND_EVERY")):128;
    int backgroundCap=getenv("BACKGROUND_CAP")?atoi(getenv("BACKGROUND_CAP")):4;
    bool backgroundStart=!getenv("BACKGROUND_START") || atoi(getenv("BACKGROUND_START"));
    long backgroundMoves=0;
    // scratch
    int64_t m1[128];
    const char* equalPartial=getenv("SAVE_EQUAL_PARTIAL");
    long equalInterval=getenv("EQUAL_INTERVAL")?atol(getenv("EQUAL_INTERVAL")):200000;
    long equalMaxHoles=getenv("EQUAL_MAX_HOLES")?atol(getenv("EQUAL_MAX_HOLES")):2;
    long lastEqualStep=0,equalSnapshots=0;
    while (true) {
        // This separate checkpoint never changes search state, RNG, or the
        // monotonically improving SAVE_PARTIAL file. The interval is a minimum
        // elapsed step count, so the first later qualifying visit is captured.
        if(equalPartial && equalInterval>0 && step-lastEqualStep>=equalInterval &&
           unc.size()>=1 && (long)unc.size()<=equalMaxHoles && (long)unc.size()==best){
            save(equalPartial);lastEqualStep=step;++equalSnapshots;
            fprintf(stderr,"EQUAL_PARTIAL count=%ld step=%ld blocks=%d holes=%zu\n",equalSnapshots,step,b,unc.size());
        }
        if (unc.empty()) {
            bestFull = b;
            char fn[256]; sprintf(fn, "shrink_cover_%d_%d_%d_%d_%u.txt", v, k, t, b, seed); save(fn);
            double el = chrono::duration<double>(chrono::steady_clock::now() - start).count();
            printf("FULL %d blocks at %.1fs\n", b, el); fflush(stdout);
            if (b <= targetB) break;
            // delete the block with fewest uniquely covered t-sets
            int bi = -1; long bl = 1L << 60;
            for (int i = 0; i < b; ++i) { long l = 0; each_all(bm[i], [&](u64 r, const int*) { if (cov[r] == 1) ++l; }); if (l < bl) { bl = l; bi = i; } }
            each_all(bm[bi], [&](u64 r, const int* S) { cover_dec(r, S, bi); });
            int last = b - 1;
            if (bi != last) {  // move block `last` into slot bi: fix sid and brk/tabu rows
                each_all(bm[last], [&](u64 r, const int*) { sid[r] += bi - last; });
                bm[bi] = bm[last];
                memcpy(&brk[(size_t)bi * 128], &brk[(size_t)last * 128], 128 * sizeof(int64_t));
                memcpy(&tabuUntil[(size_t)bi * 128], &tabuUntil[(size_t)last * 128], 128 * sizeof(int));
            }
            bm.pop_back(); --b;
            for (u64 r : unc) w[r] = 1;  // uncovered sets carry no brk weight, so this is safe
            best = unc.size();
            if (partial) save(partial);
            continue;
        }
        if ((step & 1023) == 0) {
            double el = chrono::duration<double>(chrono::steady_clock::now() - start).count();
            if (el >= nextReport) {
                fprintf(stderr, "PROGRESS b=%d best=%ld current=%zu step=%ld elapsed=%.1f\n", b, best, unc.size(), step, el);
                fflush(stderr); nextReport = el + 10.0;
            }
            if (el > secs || (maxSteps && step >= maxSteps)) break;
        }
        ++step;
#ifdef CHECK
        if (step % 5000 == 0) {  // brute-force recomputation of cov, sid and brk
            vector<uint16_t> c2(NT, 0); vector<uint32_t> s2(NT, 0);
            for (int i = 0; i < b; ++i) each_all(bm[i], [&](u64 r, const int*) { c2[r]++; s2[r] += i; });
            for (u64 r = 0; r < NT; ++r) if (c2[r] != cov[r] || s2[r] != sid[r]) { fprintf(stderr, "CHECK cov/sid mismatch at step %ld\n", step); exit(2); }
            for (int i = 0; i < b; ++i) {
                int64_t row[128] = {0};
                each_all(bm[i], [&](u64 r, const int* S) { if (cov[r] == 1) for (int a = 0; a < t; ++a) row[S[a]] += w[r]; });
                for (int x = 0; x < v; ++x) if (((bm[i] >> x) & 1) && row[x] != brk[(size_t)i * 128 + x]) { fprintf(stderr, "CHECK brk mismatch block %d point %d at step %ld\n", i, x, step); exit(2); }
            }
            if (step % 50000 == 0) fprintf(stderr, "CHECK ok at step %ld\n", step);
        }
#endif
        if(backgroundEvery>0 && ((backgroundStart && step==1) || step%backgroundEvery==0) && (int)unc.size()<=backgroundCap){
            BackgroundMove background=background_candidate(rng,backgroundCap,backgroundMoves<8);
            if(background.block>=0){
                apply_background(background);
                tabuUntil[(size_t)background.block*128+background.outgoing]=step+tenure+(int)(rng()%4);
                ++backgroundMoves;
                if(backgroundMoves<=8 || backgroundMoves%128==0)
                    fprintf(stderr,"BACKGROUND_MOVE count=%ld step=%ld row=%d outgoing=%d incoming=%d loss=%d holes=%zu\n",backgroundMoves,step,background.block,background.outgoing+1,background.incoming+1,background.loss,unc.size());
                if(!noWeight)for(u64 r:unc)++w[r];
                continue;
            }
        }
        u64 rT;
        if (U01(rng) < noise) rT = unc[rng() % unc.size()];
        else {
            rT = unc[rng() % unc.size()];
            for (int s = 0; s < 3; ++s) { u64 r2 = unc[rng() % unc.size()]; if (w[r2] > w[rT]) rT = r2; }
        }
        M T = unrank(rT);
        long bestGain = -(1L << 60); int bi = -1, bout = -1, bin_ = -1; int nties = 0;
        for (int i = 0; i < b; ++i) {
            M I = bm[i] & T;
            if (pc128(I) != t - 1) continue;
            int xin = ctz128(T & ~bm[i]);
            if (tabuUntil[(size_t)i * 128 + xin] > step) continue;
            // one pass over (t-1)-subsets R of block i: uncovered R+xin
            int P[128]; int n = pts_of(bm[i], P);
            int64_t Mall = 0;
            for (int j = 0; j < n; ++j) m1[P[j]] = 0;
            if (unc.size() < 600) {
                // Exact same make gains: visit only uncovered targets instead
                // of all triples of this block. Integer sums preserve tie order.
                M inbit = BIT(xin), allowed = bm[i] | inbit;
                for (u64 rr : unc) {
                    M target = target_mask[rr];
                    if (!(target & inbit) || (target & ~allowed)) continue;
                    int64_t ww = w[rr]; Mall += ww;
                    for (M rest = target & ~inbit; rest; rest &= rest - 1)
                        m1[ctz128(rest)] += ww;
                }
            } else if (t == 4) {
                size_t base = xin * triple_count;
                for (int a = 0; a < n - 2; ++a)
                    for (int bb = a + 1; bb < n - 1; ++bb) {
                        size_t ab = base + Cb[P[a]][1] + Cb[P[bb]][2];
                        for (int c = bb + 1; c < n; ++c) {
                            uint32_t r = rank4[ab + Cb[P[c]][3]];
                            if (cov[r] == 0) {
                                int64_t ww = w[r]; Mall += ww;
                                m1[P[a]] += ww; m1[P[bb]] += ww; m1[P[c]] += ww;
                            }
                        }
                    }
            } else subsets(n, t - 1, [&](int* idx) {
                int S[20]; int m = 0; bool placed = false;
                for (int a = 0; a < t - 1; ++a) { int q = P[idx[a]]; if (!placed && xin < q) { S[m++] = xin; placed = true; } S[m++] = q; }
                if (!placed) S[m++] = xin;
                u64 r = rank_pts(S, t);
                if (cov[r] == 0) { int64_t ww = w[r]; Mall += ww; for (int a = 0; a < t - 1; ++a) m1[P[idx[a]]] += ww; }
            });
            const int64_t* row = &brk[(size_t)i * 128];
            for (M q = bm[i] & ~T; q; q &= q - 1) {
                int xout = ctz128(q);
                long g = (Mall - m1[xout]) - row[xout];
                if (g > bestGain) { bestGain = g; bi = i; bout = xout; bin_ = xin; nties = 1; }
                else if (g == bestGain && (rng() % (++nties)) == 0) { bi = i; bout = xout; bin_ = xin; }
            }
        }
        if (bi < 0) {
            vector<int> cands; for (int i = 0; i < b; ++i) if (pc128(bm[i] & T) == t - 1) cands.push_back(i);
            if (cands.empty()) continue;
            bi = cands[rng() % cands.size()]; bin_ = ctz128(T & ~bm[bi]);
            M rest = bm[bi] & ~T; int nr = pc128(rest); int pick = rng() % nr;
            for (M q = rest; q; q &= q - 1, --pick) if (pick == 0) { bout = ctz128(q); break; }
        }
        M B = bm[bi];
        each_with(B, bout, [&](u64 r, const int* S) { cover_dec(r, S, bi); });
        M B2 = (B & ~BIT(bout)) | BIT(bin_);
        bm[bi] = B2;
        each_with(B2, bin_, [&](u64 r, const int* S) { cover_inc(r, S, bi); });
        brk[(size_t)bi * 128 + bout] = 0;
        tabuUntil[(size_t)bi * 128 + bout] = step + tenure + (int)(rng() % 4);
        if (!noWeight) for (u64 r : unc) w[r] += 1;   // NOWEIGHT=1: plain tabu search on the uncovered count (baseline)
        long c = unc.size();
        if (c < best) {
            best = c;
            if (partial) save(partial);
            fprintf(stderr, "BEST b=%d uncovered=%ld step=%ld\n", b, best, step);
            fflush(stderr);
        }
    }
    if (getenv("SAVE_FINAL")) save(getenv("SAVE_FINAL"));
    fprintf(stderr,"BACKGROUND MOVES %ld\n",backgroundMoves);
    if (bestFull > 0) printf("SHRINK result: full cover with %d blocks\n", bestFull);
    double el = chrono::duration<double>(chrono::steady_clock::now() - start).count();
    printf("WLS2 C(%d,%d,%d) b=%d seed=%u: best %ld uncovered, %ld steps, %.1fs (%.0f steps/s)\n",
           v, k, t, b, seed, best, step, el, step / max(el, 1e-9));
}

