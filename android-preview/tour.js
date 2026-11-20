/* Trialum S7 Android VISUAL PREVIEW. No game-state writes. */
(() => {
  function launch() {
    document.body.classList.add("trialum-garden-apk");
    const shell = document.createElement("div");
    shell.id = "gardenPreview";
    shell.innerHTML = [
      '<div class="gp-titlebar"><div><b>🌿 TRIALUM 3D</b><small>MASTER GARDEN · PASS 2</small></div>',
      '<span class="gp-state" id="gpStatus">Се вчитува сцената…</span></div>',
      '<div class="gp-bottom"><div class="gp-locations" id="gpLocations" aria-label="Погледи низ градината">',
      '<button data-view="overview" class="selected">🌐 Цела градина</button>',
      '<button data-view="water">💧 Водно јадро</button>',
      '<button data-view="g00l">🏗️ Сервис</button>',
      '<button data-view="door">🚪 Врата</button>',
      '<button data-view="desk">🖥️ Компјутер</button>',
      '<button data-view="bed1">🌱 G-02</button>',
      '<button data-view="bed2">🌿 G-03</button>',
      '<button data-view="bed3">🌳 G-04</button>',
      '<button data-view="bed4">🪴 G-05</button></div>',
      '<div class="gp-actions"><button id="gpEdit">✏️ Уреди ја градината</button>',
      '<button id="gpJson">💾 Зачувај JSON</button></div>',
      '<p class="gp-disclaimer">Вистински 3D визуелен преглед; симулацијата ќе се поврзе со engine по одобрен JSON.</p></div>'
    ].join("");
    document.body.appendChild(shell);
    const status=shell.querySelector("#gpStatus");
    let current="overview";
    function choose(view){
      current=view;
      shell.querySelectorAll("[data-view]").forEach(b=>b.classList.toggle("selected",b.dataset.view===view));
      if (typeof window.trialumPreviewCamera==="function") {
        try { window.trialumPreviewCamera(view); status.textContent="3D поглед · "+view; }
        catch (error) { status.textContent="Неуспешен преглед"; console.error(error); }
      } else status.textContent="Сè уште се вчитува 3D…";
    }
    shell.querySelector("#gpLocations").addEventListener("click", event=>{
      const b=event.target.closest("button[data-view]");
      if (b) choose(b.dataset.view);
    });
    shell.querySelector("#gpEdit").addEventListener("click", ()=>{
      const on=document.body.classList.toggle("gp-editing");
      shell.querySelector("#gpEdit").textContent=on?"👁️ Врати 3D преглед":"✏️ Уреди ја градината";
      requestAnimationFrame(()=>{if(!on)choose(current);});
    });
    shell.querySelector("#gpJson").addEventListener("click", ()=>{
      const button=document.getElementById("exportProject");
      if(button)button.click();
      else status.textContent="JSON извозот не е достапен";
    });
    let checks=0;
    const timer=setInterval(()=>{
      checks++;
      const s=document.getElementById("statusText")?.textContent||"";
      const count=document.getElementById("objectCounter")?.textContent||"";
      if(typeof window.trialumPreviewCamera==="function" && /подготвен|Отворена|предмети|готов/i.test(s+" "+count)) {
        choose(current);
        clearInterval(timer);
      } else if(checks>75){
        status.textContent="3D вчитувањето трае подолго — пробај хоризонтален приказ";
        clearInterval(timer);
      }
    },650);
    document.addEventListener("visibilitychange",()=>{if(!document.hidden&&typeof window.trialumPreviewCamera==="function")choose(current)});
  }
  if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",launch,{once:true});
  else launch();
})();
