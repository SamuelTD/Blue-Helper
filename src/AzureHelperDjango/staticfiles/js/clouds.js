// static/myapp/js/clouds.js

document.addEventListener("DOMContentLoaded", () => {
  const container = document.getElementById("cloud-container");
  const cloudSrc  = window.CLOUD_SRC;
  const csvUrl    = window.CLOUDS_CSV_URL;

  if (!csvUrl) {
    console.error("⚠️  CLOUDS_CSV_URL not defined on window!");
    return;
  }

  Papa.parse(csvUrl, {
    download:       true,
    skipEmptyLines: true,
    delimiter:      ";",        // <-- semicolon delimited
    header:         false,      // <-- no header row
    complete: ({ data: rows }) => {
      // rows is an array of arrays: [ [label, url], [label, url], … ]
      const clouds = rows
        .map(r => {
          const label = (r[0] || "").trim();
          const url   = (r[1] || "").trim();
          return { label, url };
        })
        .filter(r => r.label && r.url);

      if (clouds.length === 0) {
        console.error("⚠️  No valid rows in your CSV – make sure each line has `label ; url`.");
        return;
      }

      spawnClouds(clouds, container, cloudSrc);
    },
    error: err => {
      console.error("⚠️  Failed to load/parse CSV:", err);
    }
  });
});


/**
 * @param {{label:string,url:string}[]} clouds
 * @param {HTMLElement} container
 * @param {string} cloudSrc
 */
function spawnClouds(clouds, container, cloudSrc) {
  const count         = Math.floor(Math.random() * 4) + 5; // 5..8
  const positions     = [];
  const minSeparation = 15; // percent

  const dist = (a, b) => Math.hypot(a.x - b.x, a.y - b.y);

  for (let i = 0; i < count; i++) {
    let x, y, tries = 0;
    do {
      x = 5 + Math.random() * 85;
      y = 5 + Math.random() * 85;
      tries++;
    } while (
      tries < 20 &&
      positions.some(p => dist(p, { x, y }) < minSeparation)
    );
    positions.push({ x, y });

    const cloud = document.createElement("div");
    cloud.className = "cloud";
    cloud.style.top  = `${y}%`;
    cloud.style.left = `${x}%`;
    cloud.style.setProperty("--s", (1 + Math.random()).toFixed(2));

    const dx = (30 + Math.random() * 30) * (Math.random() < 0.5 ? -1 : 1) + "px";
    const dy = (30 + Math.random() * 30) * (Math.random() < 0.5 ? -1 : 1) + "px";
    cloud.style.setProperty("--dx", dx);
    cloud.style.setProperty("--dy", dy);
    cloud.style.animationDuration = (2 + Math.random() * 3).toFixed(2) + "s";

    const { label, url } = clouds[i % clouds.length];

    const link = document.createElement("a");
    link.href       = url;
    link.target     = "_blank";
    link.rel        = "noopener";
    link.className  = "block text-center hover:scale-105 transition-transform duration-300";
    link.innerHTML  = `
          <img
        src="${cloudSrc}"
        alt="cloud"
        class="w-[120px] h-auto block"
      />
      <div
        class="
          absolute inset-0
          flex items-center justify-center
          px-2
          text-sm font-semibold text-gray-700
          text-center break-words
          leading-tight
        "
      >
        ${label}
      </div>
    `;

    cloud.appendChild(link);
    container.appendChild(cloud);
  }
}
