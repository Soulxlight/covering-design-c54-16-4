// Secondary objective only: degree and pair-degree squared sums.
int pointDegree[64]={},pairDegree[64][64]={};
int balancePointWeight=16,balancePairWeight=1;
long balanceTieWins=0;
void degree_change(M block,int delta){
    int P[64],n=pts_of(block,P);
    for(int i=0;i<n;++i){pointDegree[P[i]]+=delta;
        for(int j=i+1;j<n;++j){pairDegree[P[i]][P[j]]+=delta;pairDegree[P[j]][P[i]]+=delta;}}
}
void degree_swap(M block,int outgoing,int incoming){
    --pointDegree[outgoing];++pointDegree[incoming];
    M keep=block&~BIT(outgoing);
    for(;keep;keep&=keep-1){int z=ctz128(keep);
        --pairDegree[outgoing][z];--pairDegree[z][outgoing];
        ++pairDegree[incoming][z];++pairDegree[z][incoming];}
}
int64_t balance_score(M block,int outgoing,int incoming){
    // One half of the exact change in the weighted squared-sum objective.
    int64_t delta=(int64_t)balancePointWeight*(pointDegree[incoming]-pointDegree[outgoing]+1);
    if(balancePairWeight){int pd=0;M keep=block&~BIT(outgoing);
        for(;keep;keep&=keep-1){int z=ctz128(keep);pd+=pairDegree[incoming][z]-pairDegree[outgoing][z]+1;}
        delta+=(int64_t)balancePairWeight*pd;}
    return delta;
}
void check_degrees(){
    int p[64]={},q[64][64]={};
    for(M block:bm){int P[64],n=pts_of(block,P);for(int i=0;i<n;++i){++p[P[i]];
        for(int j=i+1;j<n;++j){++q[P[i]][P[j]];++q[P[j]][P[i]];}}}
    for(int i=0;i<v;++i){if(p[i]!=pointDegree[i]){fprintf(stderr,"point-degree mismatch\n");exit(3);}
        for(int j=0;j<v;++j)if(q[i][j]!=pairDegree[i][j]){fprintf(stderr,"pair-degree mismatch\n");exit(3);}}
}
