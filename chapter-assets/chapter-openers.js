/* ENV2301 chapter photo openers and concise rendered chapter titles.
   Deliberately supplements existing Quarto sources to avoid changing Chapters 1–9. */
(function(){
  'use strict';
  const chapters={
    '01-inquiry.html':{number:1},
    '02-system-understanding.html':{number:2},
    '03-measurement.html':{number:3},
    '04-variability-uncertainty.html':{number:4},
    '05-sampling-replication.html':{number:5},
    '06-space.html':{number:6},
    '07-time.html':{number:7},
    '08-mobile-organisms.html':{number:8},
    '09-experiments.html':{number:9},
    '10-quantitative-socioenvironmental.html':{number:10},
    '11-qualitative-participatory.html':{number:11},
    '12-socioenvironmental-explanations.html':{number:12}
  };
  const filename=(location.pathname.split('/').pop()||'');const cfg=chapters[filename];if(!cfg)return;
  function decorate(){
    const hdr=document.querySelector('#title-block-header');
    const h1=(hdr&&hdr.querySelector('h1.title'))||document.querySelector('main h1.title');
    if(!hdr||!h1||document.querySelector('.chapter-opening-photo'))return;
    const figure=document.createElement('figure');figure.className='chapter-opening-photo';
    const photo=document.createElement('img'); photo.src=`chapter-assets/chapter-openers/chapter-${String(cfg.number).padStart(2,'0')}.jpg`;
    photo.alt=`Chapter ${cfg.number} opening photograph`;photo.loading='eager';photo.decoding='async';
    const cap=document.createElement('figcaption');cap.textContent='Photograph: Michiel van Breugel';
    figure.append(photo,cap);hdr.insertAdjacentElement('afterend',figure);

  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',decorate,{once:true});else decorate();
})();
