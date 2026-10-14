// Independent standard-library colex-Set verifier for the pinned335-block file.
'use strict';
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const EXPECTED = 'f00db8b4253b98fecf412031948e7de4e5c5f78a9cc021ef483bb01ea9d84bc8';
function need(ok, message) { if (!ok) throw Error(message); }
function verify(filename=path.join(__dirname, '..', 'data', 'cover-335.txt')) {
  const raw=fs.readFileSync(filename), digest=crypto.createHash('sha256').update(raw).digest('hex');
  need(raw.length===16415 && digest===EXPECTED, 'pinned witness byte identity');
  const lines=raw.toString('ascii').split('\n');
  need(lines.pop()==='' && lines.length===335, '335 lines and final LF');
  const signatures=new Set(), rows=[];
  for (let line=0;line<lines.length;line++) {
    const tokens=lines[line].trim().split(/\s+/), row=tokens.map(Number).sort((a,b)=>a-b);
    need(tokens.length===16 && tokens.every(x=>/^[0-9]{2}$/.test(x)) &&
         row.every(x=>Number.isInteger(x)&&x>=1&&x<=54) && new Set(row).size===16,
         'illegal block on line '+(line+1));
    const key=row.join(',');need(!signatures.has(key),'repeated whole block');
    signatures.add(key);rows.push(row);
  }
  const choose=Array.from({length:55},()=>Array(5).fill(0));
  for(let n=0;n<=54;n++)for(let k=0;k<=4;k++)
    choose[n][k]=k===0?1:(n===0?0:choose[n-1][k]+choose[n-1][k-1]);
  const rank=(a,b,c,d)=>choose[a-1][1]+choose[b-1][2]+choose[c-1][3]+choose[d-1][4];
  need(choose[54][4]===316251,'four-subset universe');
  const toy=new Set([rank(1,2,3,4),rank(4,5,6,7)]), toyRanks=new Set();let toyCovered=0;
  for(let a=1;a<=5;a++)for(let b=a+1;b<=6;b++)for(let c=b+1;c<=7;c++)for(let d=c+1;d<=8;d++) {
    const index=rank(a,b,c,d);
    need(index>=0&&index<70&&Number.isInteger(index)&&!toyRanks.has(index),'toy colex bijection');
    toyRanks.add(index);const yes=toy.has(index);
    need(yes===((a===1&&b===2&&c===3&&d===4)||(a===4&&b===5&&c===6&&d===7)),'toy coverage');
    if(yes)toyCovered++;
  }
  need(toyRanks.size===70&&toyCovered===2,'boundary controls');
  const present=new Set();
  for(const row of rows)for(let a=0;a<13;a++)for(let b=a+1;b<14;b++)for(let c=b+1;c<15;c++)for(let d=c+1;d<16;d++)
    present.add(rank(row[a],row[b],row[c],row[d]));
  let checked=0, covered=0;const holes=[];
  for(let a=1;a<=51;a++)for(let b=a+1;b<=52;b++)for(let c=b+1;c<=53;c++)for(let d=c+1;d<=54;d++) {
    checked++;
    if(present.has(rank(a,b,c,d)))covered++;else if(holes.length<100)holes.push([a,b,c,d]);
  }
  need(checked===316251&&covered===present.size,'complete independent traversal');
  need(covered===checked,'witness has uncovered quadruples: '+(checked-covered));
  return {status:'PASS_COMPLETE_COVER_335',method:'Node independently parsed colex-rank Set',
    witness:'data/cover-335.txt',source_sha256:digest,bytes:raw.length,points:54,block_size:16,
    legal_blocks:rows.length,distinct_blocks:signatures.size,quadruples_checked:checked,covered,
    uncovered:checked-covered,holes,control_quadruples:70,upper_bound:335,optimality_claimed:false};
}
if(require.main===module) {
  try {
    need(process.argv.length<=3,'at most one witness path');
    console.log(JSON.stringify(verify(process.argv[2]),null,2));
  } catch(error) { console.error('FAIL_CLOSED: '+error.message);process.exitCode=1; }
}
module.exports={verify};
