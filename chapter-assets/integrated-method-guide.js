/* ENV2301 Chapters 10–12 integrated research-design practice guide.
   One progressive key, revisable choices, multiple suitable approaches,
   expandable implementation guidance and matched hypothetical studies.
   No network, dependency or personal-data storage. */
(() => {
'use strict';
const root=document.getElementById('integrated-method-guide');
if(!root)return;
const chooser=root.querySelector('#integrated-choices');
const results=root.querySelector('#integrated-results');
const library=document.getElementById('integrated-source-library');
const state=['','','',''];
const questions=[
 {label:'1. What is the main question?',options:[
  ['activity','Where, when or how do people use a place?'],
  ['preference','How do people evaluate vegetation or a management proposal?'],
  ['experience','Why do experiences, choices or practices differ?'],
  ['management','How are management decisions made and put into practice?'],
  ['change','Did a management change influence people or behaviour?'],
  ['history','How did places, practices or relationships change?'],
  ['integration','How do environmental conditions, activities and experiences connect?']]},
 {label:'2. What conclusion would you like to draw?',options:[
  ['describe','Describe a pattern or set of experiences'],
  ['compare','Compare settings, times, groups or contrasting cases'],
  ['mechanism','Develop and assess explanations for the pattern'],
  ['effect','Attribute a change to an intervention or management action']]},
 {label:'3. Whose behaviour, knowledge or experience is relevant?',options:[
  ['onsite','Current visitors or people observed on site'],
  ['residents','Residents, including people who do not use the place'],
  ['actors','Managers, workers and other people involved in decisions'],
  ['mixed','Several groups, including those who may be absent']]},
 {label:'4. What sources can you reasonably use?',options:[
  ['field','Collect new observations or speak with participants'],
  ['existing','Use existing records, images or historical sources'],
  ['both','Combine new field information with existing sources']]}
];
const methods={
 count:{name:'Structured behavioural observation',short:'Record defined activities, movements or occupancy systematically across sites and times.',chapter:'10-quantitative-socioenvironmental.html#guide-method-guide-10a-fixed-point-counts-and-activity-scans',types:['quant'],details:'Define an event, spatial boundary, observation duration and effort. Sample comparable times and places. Decide whether passages, visits, people or location–time periods are the units. Record visibility and activity at each session. Repeated sightings of one person are not necessarily independent visitors.',limits:'Can describe observable use, not why people chose an activity. Consider observation effort, detectability, temporal and spatial coverage.',case:3},
 intercept:{name:'Visitor-intercept questionnaire',short:'Ask systematically approached visitors about reported preferences, activities or experiences.',chapter:'10-quantitative-socioenvironmental.html#guide-method-guide-10b-intercept-surveys',types:['quant'],details:'Define the population of visits, recruit across selected places and time periods, record eligibility, refusals and relevant exposure conditions, and use consistent questions. Specify whether the unit is a respondent, visit or rating.',limits:'On-site recruitment excludes non-users. Answers are reported experiences or intentions, not direct observations of behaviour.',case:1},
 residents:{name:'Resident or household questionnaire',short:'Reach people outside the study site, including those who do not visit it.',chapter:'10-quantitative-socioenvironmental.html#guide-method-guide-10c-residential-and-household-questionnaires',types:['quant'],details:'Define the residential population and recruitment frame. Consider how households or individuals are selected, how absent people are contacted, nonresponse and accessibility. Ask about use and non-use without presuming that all respondents are park visitors.',limits:'Coverage and participation bias can prevent inference to all residents. Questionnaire answers may not establish the underlying processes.',case:3},
 photo:{name:'Photographs or stated-choice scenarios',short:'Compare responses to clearly defined vegetation or management alternatives.',chapter:'10-quantitative-socioenvironmental.html#guide-method-guide-10d-photographs-and-stated-preference-scenarios',types:['quant'],details:'Select or create comparable scenes differing in intended attributes, pilot the scenarios and record how they are presented. Use repeated ratings or choices only when the statistical structure respects repeated responses from participants.',limits:'Preferences for images or scenarios are not necessarily choices made in a real park. Background differences between images can confound the target characteristic.',case:1},
 records:{name:'Existing activity records and automatic counters',short:'Use time-stamped records for patterns of use or change, while examining how the records were created.',chapter:'10-quantitative-socioenvironmental.html#guide-method-guide-10e-administrative-records-and-digital-traces',types:['quant'],details:'Examine how each record was generated, what it counts, changes in technology, coverage, maintenance and missingness. Obtain comparable effort and time denominators where possible.',limits:'Large datasets may still have systematic gaps. Records may represent passages, transactions or device users rather than unique people.',case:3},
 linked:{name:'Linked environmental and social measurements',short:'Measure environmental conditions and reported experiences at corresponding places and times.',chapter:'10-quantitative-socioenvironmental.html#guide-method-guide-10f-linking-environmental-exposures-to-experiences',types:['quant','combined'],details:'Link each respondent or observational session to the conditions they experienced: canopy cover, shade, surface condition, temperature, visibility and access. Preserve spatial and temporal identifiers and consider plausible confounders.',limits:'A correlation between vegetation and an experience does not, by itself, identify a causal pathway. Conditions and respondents can both be selected non-randomly.',case:3},
 interview:{name:'Semi-structured interviews',short:'Investigate how people explain decisions, experiences and meanings in their own terms.',source:'ch12-method-ch11-note-10',chapter:'11-qualitative-participatory.html#ch11-s112',types:['qual'],details:'Develop open prompts about specific occasions and places, then follow up on contrasting details. Select people with relevant variation in experiences and keep recordings, field notes and context linked.',limits:'Detailed accounts do not by themselves estimate how widespread a view is. Researcher prompts and recruitment affect what is said.',case:3},
 walk:{name:'Walking interviews',short:'Explore routes and environmental experiences while participants move through the relevant setting.',source:'ch12-method-ch11-note-13',chapter:'11-qualitative-participatory.html#ch11-s112',types:['qual'],details:'Plan accessible, safe routes; ask participants to identify meaningful locations; record when and where comments were made; compare accounts with conditions and observed choices.',limits:'People who cannot walk the route are easily excluded. A guided route may alter what participants would ordinarily do.',case:3},
 observe:{name:'Observation of practices and interactions',short:'Document routines, informal rules and actions in the settings in which they occur.',source:'ch12-method-ch11-note-12',chapter:'11-qualitative-participatory.html#ch11-s115',types:['qual'],details:'Choose relevant settings and occasions; distinguish descriptive notes from interpretations; record who was present and what the researcher could or could not observe. Compare repeated observations with participants’ accounts.',limits:'Researchers may influence behaviour. Observing an action does not necessarily reveal the actor’s reasons.',case:2},
 group:{name:'Focus groups',short:'Examine how perspectives, agreement and disagreement develop through discussion.',source:'ch12-method-ch11-note-11',chapter:'11-qualitative-participatory.html#ch11-s116',types:['qual'],details:'Choose group composition deliberately; decide whether participants need shared experience or contrasting positions. Facilitate without imposing agreement, record interaction and note who does not speak.',limits:'Status and social relationships may inhibit disagreement. A group consensus is not necessarily a community-wide view.',case:5},
 archives:{name:'Historical documents and archives',short:'Reconstruct earlier conditions, decisions and representations using records produced for different purposes.',source:'ch12-method-ch11-note-14',chapter:'11-qualitative-participatory.html#ch11-s114',types:['qual'],details:'Identify the origin, date, coverage, intended audience and omissions in each source. Compare documents and photographs with oral histories and observations where appropriate.',limits:'Records survive selectively. A missing document does not mean an event did not occur.',case:4},
 mapping:{name:'Participatory mapping',short:'Ask people to identify places, uses, barriers and competing claims on maps.',source:'ch12-method-ch11-note-15',chapter:'11-qualitative-participatory.html#ch11-s117',types:['qual','combined'],details:'Use a suitable base map, clarify which areas participants know, retain the provenance of annotations, and invite differing interpretations of the same location.',limits:'Mapped features reflect participants and the task; they do not automatically represent all residents or objectively measured conditions.',case:5},
 images:{name:'Participant-generated photographs',short:'Let participants show which environmental features or experiences they consider significant.',source:'ch12-method-ch11-note-16',chapter:'11-qualitative-participatory.html#ch11-s117',types:['qual'],details:'Agree on ethical and practical rules for making images; discuss each image with its maker; record circumstances and participants’ interpretations.',limits:'Photographed scenes are deliberately selected, not a representative inventory of environmental conditions.',case:5},
 analysis:{name:'Coding and comparing qualitative accounts',short:'Analyse differences across accounts, situations and sources to assess possible explanations.',source:'ch12-method-ch11-note-17',chapter:'12-socioenvironmental-explanations.html#ch12-analysis',types:['qual'],details:'Preserve transcripts and context; code related passages; compare within and across cases; use memos to state explanations, alternative accounts and further observations needed.',limits:'A coding scheme does not automatically yield a valid explanation. Counts of coded mentions do not measure population prevalence.',case:3}
};
const base={activity:['count','records','intercept','walk'],preference:['photo','intercept','residents','interview','walk'],experience:['interview','walk','observe','analysis','group'],management:['observe','interview','group','archives','analysis'],change:['count','records','linked','interview','intercept'],history:['archives','interview','mapping','observe'],integration:['linked','count','interview','observe','mapping']};
const escape=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function selectOptions(i){
 const q=questions[i];return `<div class="integrated-step" data-step="${i}"><label for="integrated-choice-${i}">${q.label}</label><select id="integrated-choice-${i}"><option value="">Choose one to continue…</option>${q.options.map(([v,t])=>`<option value="${v}" ${state[i]===v?'selected':''}>${t}</option>`).join('')}</select></div>`;
}
function drawSteps(){
 chooser.innerHTML=questions.map((_,i)=>i===0||state[i-1]?selectOptions(i):'').join('');
 chooser.querySelectorAll('select').forEach(sel=>sel.addEventListener('change',()=>{
  const i=Number(sel.id.split('-').pop());state[i]=sel.value;for(let j=i+1;j<state.length;j++)state[j]='';drawSteps();drawResults();
 }));
}
function scoreMethods(){
 const [focus,inference,people,sources]=state;
 const scores=new Map();const add=(ids,pts)=>ids.forEach(k=>scores.set(k,(scores.get(k)||0)+pts));
 add(base[focus]||[],5);
 if(inference==='describe')add(['count','intercept','interview','records'],2);
 if(inference==='compare')add(['count','intercept','linked','interview','analysis'],3);
 if(inference==='mechanism')add(['interview','observe','linked','walk','analysis'],4);
 if(inference==='effect')add(['count','linked','records','intercept'],4);
 if(people==='residents')add(['residents','interview','mapping'],5);
 if(people==='actors')add(['interview','observe','group','archives'],5);
 if(people==='mixed')add(['residents','interview','mapping','linked'],3);
 if(people==='onsite')add(['intercept','count','walk'],3);
 if(sources==='existing')add(['records','archives'],7);
 if(sources==='both')add(['records','archives','linked'],3);
 if(sources==='field')add(['interview','count','observe','intercept'],2);
 return [...scores].sort((a,b)=>b[1]-a[1]).map(x=>x[0]);
}
function renderMethod(k,i){
 const m=methods[k],src=library?.querySelector('#'+m.source),worked=library?.querySelector('#ch12-investigation-'+m.case);
 const fromSource=src?.querySelector('.ch11-foldable-body')?.innerHTML||'';
 const example=worked?`<details class="integrated-example"><summary>One possible related investigation (worked example)</summary><div>${worked.innerHTML.replace(/^\s*<summary[^>]*>[\s\S]*?<\/summary>/,'')}</div><p><em>This is one possible design for a related question. Your own selection and comparison should follow from the question you are trying to answer.</em></p></details>`:'';
 const expanded=`<p>${escape(m.details)}</p>${fromSource?'<div class="integrated-original-guide">'+fromSource+'</div>':''}<p><strong>What to examine carefully:</strong> ${escape(m.limits)}</p>${example}<p><a href="${escape(m.chapter)}">Read the corresponding chapter section or original method guide</a>.</p>`;
 return `<details class="integrated-method" id="integrated-method-${k}"><summary><strong>${escape(m.name)}</strong><span>${escape(m.short)}</span><small>Explore method, sampling, limitations and an example</small></summary><div class="integrated-detail">${expanded}</div></details>`;
}
function drawResults(){
 if(state.some(x=>!x)){
  results.innerHTML=state[0]?'<p class="integrated-provisional">Continue through the choices. You can revise any earlier answer, and the suggested approaches will change.</p>':'';
  return;
 }
 const [focus,inference,people,sources]=state;
 let rank=scoreMethods();
 // Ensure each shortlist contains contrasting approaches where feasible; use no more than five cards.
 let shortlist=rank.slice(0,5);
 if((inference==='mechanism'||focus==='integration'||focus==='change')&&!shortlist.some(k=>methods[k].types.includes('qual')))shortlist[4]='interview';
 if((focus==='change'||focus==='integration')&&!shortlist.some(k=>methods[k].types.includes('quant')))shortlist[4]='linked';
 shortlist=[...new Set(shortlist)];
 const notes=[];
 if(people==='onsite')notes.push('Observing or recruiting on site excludes some non-users; consider whether they are relevant to your question.');
 if(people==='residents'||people==='mixed')notes.push('If non-users are relevant, recruitment needs to extend beyond people encountered inside the site.');
 if(inference==='effect')notes.push('An intervention effect also requires a credible comparison: for example, replicated intervention and comparison sites, potentially before and after a change. A survey or interview alone cannot establish the causal effect.');
 if(inference==='compare')notes.push('Keep the sites, people or times being compared identifiable; multiple interviews at one site do not create independent replicate sites.');
 if(inference==='mechanism')notes.push('Look deliberately for observations or accounts that might distinguish competing explanations, including cases that challenge the first interpretation.');
 if(sources==='existing')notes.push('Before using historical or digital records, check how and why they were produced and which people or events they leave out.');
 let combination='Different approaches contribute different information. You might first observe patterns, use interviews to identify explanations or missing considerations, and then revise the observation or comparison design. The order can also run in the opposite direction.';
 if(focus==='preference')combination='Questionnaires or scenarios can measure reported preferences; interviews can investigate what respondents mean by their answers. Actual route use or activities require an additional observational component.';
 if(focus==='change')combination='Plan the intervention comparison before choosing instruments. Repeated observations or records can document change; interviews can investigate what people noticed or why their behaviour may have changed.';
 if(focus==='history')combination='Use records and oral histories for different aspects of past change. Participant mapping and contemporary observations can help locate, compare and question interpretations of those sources.';
 if(focus==='management')combination='Observe practices, ask participants about decisions and compare their accounts with formal rules or records. Agreement between sources does not establish that they are independent.';
 results.innerHTML=`<div class="integrated-summary"><h4>Approaches to consider</h4><p>You have selected <strong>${escape(questions[0].options.find(x=>x[0]===focus)[1])}</strong> and an aim to <strong>${escape(questions[1].options.find(x=>x[0]===inference)[1].toLowerCase())}</strong>. The options below are a shortlist, not a ranking of universally best methods. Several may be combined.</p></div>`+
 shortlist.map(renderMethod).join('')+`<div class="integrated-combination"><h4>Combining methods and revisiting decisions</h4><p>${escape(combination)}</p>${notes.map(x=>'<p>'+escape(x)+'</p>').join('')}<p>Compare what each approach records, which sampling units it requires, and which explanations its observations can distinguish. If the result does not support the intended conclusion, change an earlier choice and inspect the alternatives.</p><button type="button" id="integrated-start-over">Start another design</button></div>`;
 results.querySelector('#integrated-start-over')?.addEventListener('click',()=>{state.fill('');drawSteps();drawResults();root.scrollIntoView({block:'start',behavior:'smooth'});});
}
drawSteps();drawResults();
})();
