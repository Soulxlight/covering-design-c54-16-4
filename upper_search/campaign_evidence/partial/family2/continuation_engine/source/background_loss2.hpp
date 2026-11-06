// Diversification outside the usual repair neighborhood. Prefer zero-private
// point removals, otherwise one-private removals, optionally mixing two-private
// removals. Incoming points deliberately
// cover no current hole, so the exact defect increase equals the private loss.
struct BackgroundMove {int block=-1,outgoing=-1,incoming=-1,loss=0;int64_t weightedLoss=0;};
BackgroundMove background_candidate(mt19937_64& rng,int cap,bool log) {
    BackgroundMove answer;
    if((int)unc.size()>cap)return answer;
    static int maxLoss=getenv("BACKGROUND_MAX_LOSS")?max(0,min(2,atoi(getenv("BACKGROUND_MAX_LOSS")))):1;
    static double loss2Probability=getenv("BACKGROUND_LOSS2_PROB")?max(0.0,min(1.0,atof(getenv("BACKGROUND_LOSS2_PROB")))):0.20;
    vector<BackgroundMove> zero,one,two;
    M universe=v==64?~(M)0:BIT(v)-1;
    for(int j=0;j<b;++j){
        int privateCount[128]={};
        each_all(bm[j],[&](u64 r,const int*S){if(cov[r]==1)for(int a=0;a<t;++a)++privateCount[S[a]];});
        for(M q=bm[j];q;q&=q-1){int outgoing=ctz128(q),loss=privateCount[outgoing];
            if(loss>maxLoss || (int)unc.size()+loss>cap)continue;
            M keep=bm[j]&~BIT(outgoing);
            for(M choices=universe&~bm[j];choices;choices&=choices-1){int incoming=ctz128(choices);
                if(tabuUntil[(size_t)j*128+incoming]>step)continue;
                M neo=keep|BIT(incoming);bool repairs=false;
                for(u64 r:unc)if(!(target_mask[r]&~neo)){repairs=true;break;}
                if(repairs)continue;
                BackgroundMove move={j,outgoing,incoming,loss,brk[(size_t)j*128+outgoing]};
                (loss==0?zero:(loss==1?one:two)).push_back(move);
            }
        }
    }
    if(log)fprintf(stderr,"BACKGROUND_CANDIDATES step=%ld holes=%zu zero=%zu one=%zu two=%zu cap=%d max_loss=%d\n",step,unc.size(),zero.size(),one.size(),two.size(),cap,maxLoss);
    if(!zero.empty())return zero[rng()%zero.size()];
    if(!two.empty() && (one.empty() || (loss2Probability>0 && (loss2Probability>=1 || uniform_real_distribution<double>(0,1)(rng)<loss2Probability))))
        return two[rng()%two.size()];
    if(!one.empty())return one[rng()%one.size()];
    return answer;
}
void apply_background(const BackgroundMove& move) {
#ifdef CHECK_BACKGROUND
    size_t beforeCount=unc.size();int64_t beforeWeight=0;
    for(u64 r:unc)beforeWeight+=w[r];
#endif
    int j=move.block;M old=bm[j];
    each_with(old,move.outgoing,[&](u64 r,const int*S){cover_dec(r,S,j);});
    bm[j]=(old&~BIT(move.outgoing))|BIT(move.incoming);
    each_with(bm[j],move.incoming,[&](u64 r,const int*S){cover_inc(r,S,j);});
    brk[(size_t)j*128+move.outgoing]=0;
#ifdef CHECK_BACKGROUND
    int64_t afterWeight=0;for(u64 r:unc)afterWeight+=w[r];
    if(unc.size()!=beforeCount+move.loss || afterWeight-beforeWeight!=move.weightedLoss){
        fprintf(stderr,"BACKGROUND exact count/weighted-loss mismatch\n");exit(3);
    }
#endif
}
