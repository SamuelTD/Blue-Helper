// static/js/clouds.js

document.addEventListener("DOMContentLoaded", () => {
  const container = document.getElementById("cloud-container");
  const wrapper   = container.parentElement;
  const cloudSrc  = window.CLOUD_SRC;
  const csvUrl    = window.CLOUDS_CSV_URL;

  if (!csvUrl) {
    console.error("CLOUDS_CSV_URL not defined!");
    return;
  }

  Papa.parse(csvUrl, {
    download:       true,
    skipEmptyLines: true,
    delimiter:      ";",
    header:         false,
    complete: ({ data: rows }) => {
      const clouds = rows
        .map(r => ({ label: (r[0]||"").trim(), url: (r[1]||"").trim() }))
        .filter(r => r.label && r.url);

      if (!clouds.length) {
        console.error("No valid CSV rows (`label ; url`).");
        return;
      }

      prepareAndSpawn(clouds, container, wrapper, cloudSrc);
    },
    error: err => console.error("CSV load error:", err)
  });
});


async function prepareAndSpawn(clouds, container, wrapper, cloudSrc) {
  const wrapRect = wrapper.getBoundingClientRect();
  const cardRect = document.getElementById("central-card").getBoundingClientRect();
  const maxOffset = 60;

  // measure default cloud (wait for it to load!)
  const tmp = document.createElement("img");
  tmp.src           = cloudSrc;
  tmp.style.cssText = "position:absolute;visibility:hidden;width:120px;";
  wrapper.appendChild(tmp);

  // Wait for the image to decode (load) before measuring
  if (tmp.decode) {
    await tmp.decode();
  } else {
    await new Promise(resolve => {
      if (tmp.complete) return resolve();
      tmp.onload  = resolve;
      tmp.onerror = resolve;
    });
  }

  // Now that it's loaded, measure its real height
  const cRect = tmp.getBoundingClientRect();
  wrapper.removeChild(tmp);

  const defaultW = cRect.width;
  const defaultH = cRect.height;

  // forbidden zone
  const forbidden = {
    xMin: cardRect.left - defaultW - maxOffset,
    xMax: cardRect.right + maxOffset,
    yMin: cardRect.top  - defaultH - maxOffset,
    yMax: cardRect.bottom + maxOffset
  };

  spawnClouds(
    clouds, container, wrapRect, forbidden,
    defaultW, defaultH, 0.15 * wrapRect.width,
    maxOffset, cloudSrc
  );
}


function spawnClouds(
  clouds, container, wrapRect, forbidden,
  defaultW, defaultH, sepPx, maxOffset, cloudSrc
) {
  const count   = Math.floor(Math.random() * 4) + 5;
  const centers = [];

  for (let i = 0; i < count; i++) {
    const { label, url } = clouds[i % clouds.length];

    // size cloud based on label length, cap at 130%
    const approxCharWidth = 8;
    const padding         = 20;
    const neededW = label.length * approxCharWidth + padding;
    let cw = Math.max(defaultW, neededW);
    cw = Math.min(cw, defaultW * 1.3);
    const ch = defaultH;

    // pick a valid (x,y)
    let x, y, tries = 0;
    while (tries++ < 100) {
      x = wrapRect.left + Math.random() * (wrapRect.width  - cw);
      y = wrapRect.top  + Math.random() * (wrapRect.height - ch);

      if (
        x > forbidden.xMin && x < forbidden.xMax &&
        y > forbidden.yMin && y < forbidden.yMax
      ) continue;

      const cx = x + cw/2, cy = y + ch/2;
      if (centers.some(p => Math.hypot(p.x - cx, p.y - cy) < sepPx)) {
        continue;
      }
      centers.push({ x: cx, y: cy });
      break;
    }
    if (tries >= 100) {
      console.warn("Couldn’t place cloud #" + i);
      continue;
    }

    // to % coords
    const leftPct = ((x - wrapRect.left) / wrapRect.width)  * 100;
    const topPct  = ((y - wrapRect.top)  / wrapRect.height) * 100;

    // build cloud
    const cloud = document.createElement("div");
    cloud.className = "cloud relative";
    cloud.style.width    = `${cw}px`;
    cloud.style.height   = `${ch}px`;
    cloud.style.top      = `${topPct}%`;
    cloud.style.left     = `${leftPct}%`;
    cloud.style.setProperty("--s", (1 + Math.random()).toFixed(2));

    const dx = (30 + Math.random()*30)*(Math.random()<0.5?-1:1) + "px";
    const dy = (30 + Math.random()*30)*(Math.random()<0.5?-1:1) + "px";
    cloud.style.setProperty("--dx", dx);
    cloud.style.setProperty("--dy", dy);
    cloud.style.animationDuration = (2 + Math.random()*3).toFixed(2) + "s";

    // inject image + centered label via CSS Grid
    cloud.innerHTML = `
  <a href="${url}" target="_blank" rel="noopener" class="block">
    <img
      src="${cloudSrc}"
      alt="cloud"
      style="display:block; width:${cw}px; height:auto;"
    />
    <div style="
      position: absolute;
      top: 50%;
      left: 50%;
      width: 85%;
      height: 85%;
      transform: translate(-50%, -30%);
      display: grid;
      place-items: center;
      padding: 0 0.5rem;
      font-size: 0.875rem;
      font-weight: 600;
      text-align: center;
      word-break: break-word;
      line-height: 1.1;
      color: var(--secondary-color);
      z-index: 1;
    ">
      ${label}
    </div>
  </a>
`;
    container.appendChild(cloud);
  }
}
