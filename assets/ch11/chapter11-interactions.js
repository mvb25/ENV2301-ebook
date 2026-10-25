(function(){
'use strict';
function initialize(){
 document.querySelectorAll('.ch11-exercise').forEach(function(box){
  var input=box.querySelector('textarea'),button=box.querySelector('.ch11-reveal'),solution=box.querySelector('.ch11-solution'),counter=box.querySelector('.ch11-count');
  if(!input||!button||!solution)return;
  var count=function(){var n=(input.value.trim().match(/\S+/g)||[]).length; if(counter)counter.textContent=n+' words · write at least 18 to reveal';button.disabled=n<18;};
  input.addEventListener('input',count);count();
  button.addEventListener('click',function(){if(button.disabled)return;var open=!solution.hidden;solution.hidden=open;button.textContent=open?'Show suggested response':'Hide suggested response';button.setAttribute('aria-expanded',String(!open));});
 });
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',initialize);else initialize();
})();


(function(){
'use strict';
const byId = id => document.getElementById(id);
const fields=['ch11-k-goal','ch11-k-setting','ch11-k-people','ch11-k-claim'];
const guide={
 interview:{id:'ch11-note-10', section:'ch11-s112',name:'Interviews',contribution:'Accounts of choices, experiences and meanings; preserve the circumstances and follow-up questions.',example:['talal2021','Talal et al. (2021)'],practical:['newing2011','Newing (2011)'],advanced:['brinkmannkvale2014','Brinkmann and Kvale (2014)']},
 group:{id:'ch11-note-11', section:'ch11-s116',name:'Focus groups',contribution:'What participants say in response to each other: agreement, disagreement, shared categories and silence.',example:['sefcik2019','Sefcik et al. (2019)'],practical:['kruegercasey2014','Krueger and Casey (2014)']},
 observe:{id:'ch11-note-12', section:'ch11-s115',name:'Observation and ethnography',contribution:'Practices, interactions, routines and informal rules in the settings where they occur.',example:['montefrio2021','Montefrio et al. (2021)'],practical:['hammersley2019','Hammersley and Atkinson (2019)']},
 walk:{id:'ch11-note-13', section:'ch11-s112',name:'Walking interviews',contribution:'Situated accounts of routes, landmarks, sensory conditions and experiences as they arise along a route.',practical:['kusenbach2003','Kusenbach (2003)'],example:['talal2021','Talal et al. (2021), for situated park interviewing']},
 archive:{id:'ch11-note-14', section:'ch11-s114',name:'Archives and historical records',contribution:'Traces of earlier environmental conditions, official decisions and cultural representations, each produced for a purpose.',example:['thiagarajah2015','Thiagarajah et al. (2015)'],practical:['newing2011','Newing (2011)']},
 map:{id:'ch11-note-15', section:'ch11-s117',name:'Participatory mapping',contribution:'Participant-defined places, activities, routes and overlapping claims; record whose annotations are whose.',practical:['brownkytta2014','Brown and Kyttä (2014)'],advanced:['reed2008','Reed (2008)']},
 photovoice:{id:'ch11-note-16', section:'ch11-s117',name:'Participant-generated images',contribution:'Features participants select as meaningful, together with their own interpretations of the photographs.',practical:['wangburris1997','Wang and Burris (1997)']},
 analyse:{id:'ch11-note-17', section:'ch11-s119',name:'Coding and qualitative analysis',contribution:'Systematic comparison across accounts, settings and sources to develop and examine explanations.',example:['talal2021','Talal et al. (2021), coded park interviews'],practical:['gale2013','Gale et al. (2013), a worked matrix-based method'],advanced:['braunclarke2021','Braun and Clarke (2021), different analytical traditions']}
};
const plan={
 experience:{methods:['interview','walk','analyse'],reason:'Start with a concrete recent occasion and let the participant identify the places and conditions that influenced it. Introduce your suspected explanation only after hearing the first account.',recruit:'Interview people whose relevant experiences differ, for example visitors who use different routes or times; reach non-users away from the study site when they are relevant.',test:'Compare how accounts relate to actual places and observed practices. Does the proposed explanation still fit someone whose choices differ?'},
 practice:{methods:['observe','interview','archive','analyse'],reason:'Observe what people do over time and discuss why, including informal arrangements and official rules. The observable practice and its reported rationale may differ.',recruit:'Include people who carry out the practice and those who organise or regulate it; consider different shifts or events.',test:'Compare field notes, participants’ accounts and records of management decisions. Look for cases where the same practice has different causes.'},
 interaction:{methods:['group','observe','analyse'],reason:'Record how shared understandings and disagreements develop during discussion, not just the final opinion of each participant.',recruit:'Choose group composition deliberately; consider whether status or prior relationships may discourage disagreement.',test:'Note who speaks, whose examples redirect the conversation and which disagreements persist or disappear.'},
 past:{methods:['archive','interview','analyse'],reason:'Use oral histories to investigate remembered experiences and documents to reconstruct dates, decisions and changes; identify what each source actually records.',recruit:'Consider different generations, users and knowledge holders, and which voices are absent from available archives.',test:'Check dates and locations against independent sources where possible, while keeping differences in interpretation visible.'},
 place:{methods:['map','walk','photovoice','analyse'],reason:'Ask people to identify meaningful locations or barriers and explain why they matter; treat disagreement about the same place as information.',recruit:'Invite groups with different routes, mobility requirements, uses and relationships with the area.',test:'Compare mapped claims with observation and environmental data where relevant; do not assume a collective map represents everyone.'},
 explain:{methods:['interview','observe','analyse'],reason:'Begin from a measured pattern, investigate different proposed mechanisms and deliberately recruit cases where your initial explanation might fail.',recruit:'Sample across the conditions and groups that could change the relationship, including people absent during the quantitative observations.',test:'Confirm spatial and temporal correspondence before comparing counts, participant accounts and environmental measurements.'}
};
function list(items){return '<ul>'+items.map(x=>'<li>'+x+'</li>').join('')+'</ul>';}
function run(){
 if(!byId(fields[0]))return;
 const [goal,setting,people,claim]=fields.map(id=>byId(id).value);
 const out=byId('ch11-k-output');
 const reset=byId('ch11-key-reset');
 const holder=byId('ch11-matched-guides');
 const nodes=holder?[...holder.querySelectorAll('details')]:[];
 if(!goal){
  if(out){out.innerHTML='';out.hidden=true;}
  if(reset)reset.hidden=true;
  if(holder)holder.hidden=true;
  nodes.forEach(el=>{el.hidden=true;el.open=false;});
  return;
 }
 if(out)out.hidden=false;
 if(reset)reset.hidden=false;
 const p=plan[goal],selected=[...p.methods],extra=[],cautions=[];
 const add=k=>{if(!selected.includes(k))selected.push(k);};
 if(setting==='group')add('group');
 if(setting==='inplace'){add('walk');add('observe');}
 if(setting==='individual')add('interview');
 if(setting==='records')add('archive');
 if(people==='sensitive'){
   cautions.push('A group setting could inhibit disclosure or dissent. Consider confidential interviews, carefully chosen recruitment routes and the participant’s control over recording.');
   if(goal!=='interaction'){let at=selected.indexOf('group');if(at>=0)selected.splice(at,1);}
 }
 if(people==='excluded')cautions.push('Recruitment only among people already using the park cannot reach people who avoid it or cannot enter. Plan a route beyond park visitors.');
 if(people==='community'){add('map');extra.push('Decide which choices participants can influence: questions, evidence collection, analysis, interpretation or the use of findings (Section 11.8).');}
 if(claim==='prevalence')cautions.push('Interviews and purposive cases do not estimate what fraction of a population holds a view. Design a suitably sampled survey if that percentage is needed (Chapter 10).');
 if(claim==='cause')cautions.push('Interview evidence can identify plausible mechanisms, but attributing a management effect requires an appropriate intervention or comparison design (Chapter 9).');
 if(claim==='change') {add('archive');extra.push('Document which records were created in each period and what changed in the process of recording or preservation (Section 11.4).');}
 if(selected.includes('map'))extra.push('If participants map overlapping uses or concerns, retain who supplied each layer and whether they were free to disagree.');
 const cite=(entry,label)=>entry ? '<a href="#ref-'+entry[0]+'">'+label+': '+entry[1]+'</a>' : '';
 const links=list(selected.map(k=>{
  const g=guide[k];const reading=[cite(g.example,'Published example'),cite(g.practical,'Practical method guidance'),cite(g.advanced,'Further interpretation')].filter(Boolean).join(' · ');
  return '<a href="#'+g.section+'">Section on '+g.name+'</a> · <a href="#'+g.id+'" data-guide="'+g.id+'">optional method guide</a><div class="ch11-method-why">'+g.contribution+'<br><small>'+reading+'</small></div>';
 }));
 if(!out)return;
 out.innerHTML='<p class="ch11-guide-provisional">'+(fields.every(id=>byId(id).value)?'Based on your four choices. Review the alternatives below.':'Provisional suggestions based on your initial choice; other selections will refine them.')+'</p><p><strong>Where to begin</strong> '+p.reason+'</p>'+
 '<strong>Methods to consider, with chapter links and reading</strong>'+links+
 '<strong>Who to recruit, and why</strong><p>'+p.recruit+'</p>'+
 '<strong>How to analyse and challenge the explanation</strong><p>'+p.test+' See <a href="#ch11-s119">Section 11.9</a> on analysis and <a href="#ch11-s1110">Section 11.10</a> on evaluating interpretations.</p>'+
 (extra.length?'<strong>Additional design choices</strong>'+list(extra):'')+
 (cautions.length?'<strong>Limits and additional methods</strong>'+list(cautions):'')+
 '<p>For recruitment and how to adapt a sample, see <a href="#ch11-s113">Section 11.3</a>. Revisit the decisions when field evidence changes your understanding.</p>'; 
 if(holder){
  holder.hidden=false;
  nodes.forEach(el=>{ const key=Object.keys(guide).find(k=>guide[k].id===el.id);
   const relevant=(key && selected.includes(key)) || (el.id==='ch11-guide-example-park' && (goal==='experience'||goal==='explain'));
   el.hidden=!relevant; if(!relevant)el.open=false;
  });
 }
 out.querySelectorAll('[data-guide]').forEach(a=>a.addEventListener('click',()=>{
   const target=byId(a.getAttribute('data-guide'));if(target?.tagName.toLowerCase()==='details')target.open=true;
 }));
}
function initialize(){
 if(!byId('ch11-method-key'))return;
 const holder=byId('ch11-matched-guides');
 if(holder){ Object.values(guide).forEach(g=>{const el=byId(g.id);if(el){el.hidden=true;holder.appendChild(el);}});
   const ex=byId('ch11-guide-example-park');if(ex){ex.hidden=true;holder.appendChild(ex);}}
 fields.forEach(id=>byId(id)?.addEventListener('change',run));
 byId('ch11-key-reset')?.addEventListener('click',()=>{
  fields.forEach(id=>{if(byId(id))byId(id).selectedIndex=0;});run();byId('ch11-method-key')?.scrollIntoView({block:'start'});
 });run();
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',initialize);else initialize();
})();
