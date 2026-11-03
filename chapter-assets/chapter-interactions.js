(() => {
function initExercises(){
 document.querySelectorAll('.ch11-exercise,.test-your-understanding').forEach((ex,i)=>{
  if(ex.querySelector('textarea') === null)return;
  const t=ex.querySelector('textarea');const b=ex.querySelector('button.ch11-reveal');
  const solution=ex.querySelector('.ch11-solution,.exercise-solution');
  if(!b||!solution)return;
  solution.hidden=true;b.disabled=true;
  const count=ex.querySelector('.ch11-count');
  const update=()=>{let s=t.value.trim();let wc=s?s.split(/\s+/).length:0;if(count)count.textContent=wc+' words';b.disabled=s.length<10;
   let status=ex.querySelector('.answer-status');if(status&&solution.hidden)status.textContent=b.disabled?'Write your answer before revealing the suggested response.':'You can now reveal the suggested response.';
  };
  t.addEventListener('input',update);update();
  b.addEventListener('click',()=>{if(b.disabled)return;solution.hidden=false;b.textContent='Suggested response shown';b.setAttribute('aria-expanded','true');b.disabled=true;ex.setAttribute('data-answered','true');});
 });
}
function initNavigation(){
 const tog=document.getElementById('nav-toggle');const side=document.getElementById('book-nav');
 if(tog&&side){tog.addEventListener('click',()=>{const isOpen=side.classList.toggle('is-open');tog.setAttribute('aria-expanded',String(isOpen));});}
 const links=[...document.querySelectorAll('#page-toc a')];
 const observer=new IntersectionObserver(entries=>{
  const current=entries.filter(x=>x.isIntersecting).sort((a,b)=>a.boundingClientRect.top-b.boundingClientRect.top)[0];
  if(!current)return;links.forEach(a=>a.classList.toggle('toc-active',a.getAttribute('href')==='#'+current.target.id));
 },{rootMargin:'-3% 0px -80% 0px'});
 document.querySelectorAll('#book-main h2[id],#book-main h3[id]').forEach(e=>observer.observe(e));
}
function initFigures(){
 const dialog=document.querySelector('.figure-dialog');if(!dialog)return;
 const big=dialog.querySelector('img');const cap=dialog.querySelector('p');
 document.querySelectorAll('figure .figure-enlarge').forEach(b=>b.addEventListener('click',()=>{
  const figure=b.closest('figure');const small=figure.querySelector('img');const caption=figure.querySelector('figcaption,.figure-caption');
  if(!small)return;big.src=small.src;big.alt=small.alt||'Enlarged figure';cap.textContent=caption?caption.textContent:'';
  dialog.showModal();
 }));
 dialog.querySelector('.figure-close').addEventListener('click',()=>dialog.close());
}
document.addEventListener('DOMContentLoaded',()=>{initExercises();initNavigation();initFigures();});
})();