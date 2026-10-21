
(function(){
const $=id=>document.getElementById(id), controls=['k_goal','k_target','k_evidence','k_design'];
const links={"10A": "guide-method-guide-10a-fixed-point-counts-and-activity-scans", "10B": "guide-method-guide-10b-intercept-surveys", "10C": "guide-method-guide-10c-residential-and-household-questionnaires", "10D": "guide-method-guide-10d-photographs-and-stated-preference-scenarios", "10E": "guide-method-guide-10e-administrative-records-and-digital-traces", "10F": "guide-method-guide-10f-linking-environmental-exposures-to-experiences"};
function link(code,label){return '<li><a href="#'+(links[code]||'')+'" data-open="'+code+'">'+label+'</a></li>'}
function run(){
 const goal=$('k_goal').value,target=$('k_target').value,evidence=$('k_evidence').value,design=$('k_design').value;
 let m=[],reason=[],warning=[];
 if(goal==='activity'||goal==='pattern'||goal==='change')m.push(['10A','Structured observation of events or occupancy']);
 if(goal==='report'||goal==='absence'||goal==='change')m.push([target==='residents'?'10C':'10B',target==='residents'?'Resident or household questionnaire':'Systematic visitor-intercept survey']);
 if(goal==='report'||goal==='change')m.push(['10D','Photographic comparison or clearly specified management scenario']);
 if(goal==='absence'){m.push(['10C','Residential sample reaching people who do not visit']);reason.push('Recruit outside the park; a visitor-intercept survey excludes some people whose absence needs explaining.');}
 if(evidence==='records'||evidence==='both')m.push(['10E','Existing records, automated counts and digital traces']);
 if(goal==='report'||goal==='change')m.push(['10F','Linked environmental conditions and reported experiences']);
 if(target==='sites')reason.push('The relevant sample includes independent locations and times; individual passersby are not independent replicate sites.');
 else if(target==='units')reason.push('The intervention unit may be a park or neighbourhood; repeated respondents within it do not create replicate intervention units.');
 else if(target==='residents')reason.push('Use a residential recruitment frame that includes non-visitors and people not currently able to access the place.');
 else reason.push('State whether you count unique people, visits, passages, activity episodes or location–time observations.');
 if(design==='effect'){warning.push('Evaluating an intervention requires a credible comparison, such as repeated pre/post measures with control areas or an experimental or quasi-experimental allocation. A method for collecting counts alone does not identify a causal effect.');}
 if(design==='groups')reason.push('Compare equivalent observation effort and time strata, and retain identifiers for repeated measures.');
 if(goal==='pattern')reason.push('Preserve dates and observation effort; do not confuse a long record at one site with spatial replication.');
 if(goal==='report')warning.push('Reported preferences measure what respondents say under a defined instrument; they do not directly measure actual behaviour.');
 if(evidence==='records')warning.push('Check what originally created each record, changes in coverage and technologies, and privacy restrictions before interpreting trends.');
 const u=[...new Map(m.map(x=>[x[0],x])).values()];
 $('k_output').innerHTML='<strong>Potential methods (open the method guides):</strong><ul>'+u.map(x=>link(x[0],x[1])).join('')+'</ul><strong>Before collecting data:</strong><ul>'+reason.map(x=>'<li>'+x+'</li>').join('')+'</ul>'+warning.map(x=>'<p class="key-warning">'+x+'</p>').join('');
 $('k_output').querySelectorAll('[data-open]').forEach(a=>a.addEventListener('click',()=>{const el=document.getElementById(links[a.dataset.open]);if(el)el.open=true;}));
}
controls.forEach(id=>$(id)?.addEventListener('change',run)); if($('k_goal'))run();
document.querySelectorAll('.restart-method-key').forEach(btn=>btn.addEventListener('click',()=>{
  controls.forEach(id=>{if($(id))$(id).selectedIndex=0;}); run();
  const key=$('research-method-key');if(key){key.scrollIntoView({behavior:'smooth',block:'start'});}
}));
})();

(function(){
  const minimumWords=25;
  const wordCount=(s)=>{const t=s.trim();return t?t.split(/\s+/u).filter(Boolean).length:0;};
  document.querySelectorAll('.self-test').forEach(box=>{
    const field=box.querySelector('.test-response');
    const counter=box.querySelector('.word-counter');
    const submit=box.querySelector('.test-submit');
    const reveal=box.querySelector('.test-reveal');
    const answer=box.querySelector('.test-answer');
    if(!field||!submit||!reveal||!answer)return;
    function update(){
      const n=wordCount(field.value);
      counter.textContent=n+' / '+minimumWords+' words';
      submit.disabled=(n<minimumWords);
      reveal.hidden=true;
      reveal.setAttribute('aria-expanded','false');
      reveal.textContent='Show suggested explanation';
      answer.hidden=true;
    }
    field.addEventListener('input',update);
    submit.addEventListener('click',()=>{
      if(wordCount(field.value)<minimumWords)return;
      reveal.hidden=false;
      reveal.focus();
    });
    reveal.addEventListener('click',()=>{
      answer.hidden=!answer.hidden;
      const expanded=!answer.hidden;
      reveal.setAttribute('aria-expanded',expanded?'true':'false');
      reveal.textContent=expanded?'Hide suggested explanation':'Show suggested explanation';
    });
    update();
  });
})();
