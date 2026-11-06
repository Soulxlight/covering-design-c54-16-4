// Exact fixed-deficit lower screen for binary a<->b switches in uniform rows.
#include <array>
#include <vector>
#include <fstream>
#include <sstream>
#include <iostream>
#include <cstdint>
#include <algorithm>
#include <chrono>
using namespace std;using U=uint64_t;using R=array<U,8>;
struct Triple{U mask;R rows;};
int main(int argc,char**argv){
 if(argc!=5){cerr<<"usage: screen v k input output.json\n";return 2;}
 int v=stoi(argv[1]),k=stoi(argv[2]);if(v>54||v<4||k<4||k>v)return 2;
 ifstream in(argv[3]);if(!in)return 2;vector<U> blocks;string line;
 while(getline(in,line)){if(line.empty()||line[0]=='#')continue;istringstream s(line);U m=0;int x,n=0;while(s>>x){if(x<1||x>v||(m>>(x-1)&1))return 2;m|=U(1)<<(x-1);++n;}if(!s.eof()||n!=k)return 2;blocks.push_back(m);}
 if(blocks.empty()||blocks.size()>512)return 2;int W=(blocks.size()+63)/64;vector<R> col(v,R{});
 for(int i=0;i<(int)blocks.size();++i)for(int x=0;x<v;++x)if(blocks[i]>>x&1)col[x][i/64]|=U(1)<<(i%64);
 vector<Triple> triples;for(int a=0;a<v-2;++a)for(int b=a+1;b<v-1;++b)for(int c=b+1;c<v;++c){Triple q{(U(1)<<a)|(U(1)<<b)|(U(1)<<c),R{}};for(int w=0;w<W;++w)q.rows[w]=col[a][w]&col[b][w]&col[c][w];triples.push_back(q);}
 vector<U> holes;for(int a=0;a<v-3;++a)for(int b=a+1;b<v-2;++b)for(int c=b+1;c<v-1;++c)for(int d=c+1;d<v;++d){bool hit=false;for(int w=0;w<W;++w)hit|=(col[a][w]&col[b][w]&col[c][w]&col[d][w])!=0;if(!hit)holes.push_back((U(1)<<a)|(U(1)<<b)|(U(1)<<c)|(U(1)<<d));}
 ofstream out(argv[4]);out<<"{\"v\":"<<v<<",\"k\":"<<k<<",\"rows\":"<<blocks.size()<<",\"holes\":"<<holes.size()<<",\"pairs\":[";bool first=true;int promising=0,minFixed=holes.size();
 for(int a=0;a<v-1;++a)for(int b=a+1;b<v;++b){
  R both{},ex{};int nex=0;U ab=(U(1)<<a)|(U(1)<<b);for(int w=0;w<W;++w){both[w]=col[a][w]&col[b][w];ex[w]=col[a][w]^col[b][w];nex+=__builtin_popcountll(ex[w]);}
  int inv=0,empty=0,single=0,current=0;
  for(U h:holes)inv+=__builtin_popcountll(h&ab)!=1;
  for(const auto&q:triples){if(q.mask&ab)continue;bool autoCovered=false;for(int w=0;w<W;++w)if(q.rows[w]&both[w]){autoCovered=true;break;}if(autoCovered)continue;
   int n=0;bool ha=false,hb=false;for(int w=0;w<W;++w){n+=__builtin_popcountll(q.rows[w]&ex[w]);ha|=(q.rows[w]&col[a][w])!=0;hb|=(q.rows[w]&col[b][w])!=0;}
   empty+=n==0;single+=n==1;current+=!ha;current+=!hb;
  }
  int fixed=inv+2*empty+single;if(inv+current!=(int)holes.size()||fixed>(int)holes.size()){cerr<<"score mismatch "<<a<<' '<<b<<'\n';return 3;}
  minFixed=min(minFixed,fixed);promising+=fixed<(int)holes.size();
  if(!first)out<<',';first=false;out<<"{\"a\":"<<a+1<<",\"b\":"<<b+1<<",\"exclusive_rows\":"<<nex<<",\"invariant_holes\":"<<inv<<",\"empty_supports\":"<<empty<<",\"singleton_supports\":"<<single<<",\"fixed_lower_bound\":"<<fixed<<",\"current_variable_deficit\":"<<holes.size()-fixed<<'}';
 }
 out<<"],\"promising_pairs\":"<<promising<<",\"minimum_fixed_bound\":"<<minFixed<<",\"all_original_assignments_checked\":true}\n";cerr<<"rows="<<blocks.size()<<" holes="<<holes.size()<<" promising="<<promising<<" minimum_fixed="<<minFixed<<'\n';
}
