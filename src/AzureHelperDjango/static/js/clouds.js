document.addEventListener("DOMContentLoaded", () => {
  const container = document.getElementById("cloud-container");
  const cloudSrc = window.CLOUD_SRC;
  const labels = ["Alpha","Beta","Gamma","Delta","Epsilon","Zeta","Eta","Theta"];
  const count = Math.floor(Math.random() * 4) + 5; // 5..8

  // keep track of existing cloud centers (in % units)
  const positions = [];
  const minSeparation = 15; // minimum distance in % between any two clouds

  // helper to compute 2D distance in percentage space
  function dist(a, b) {
    const dx = a.x - b.x;
    const dy = a.y - b.y;
    return Math.sqrt(dx*dx + dy*dy);
  }

  for (let i = 0; i < count; i++) {
    let x, y, tries = 0;

    // find a position at least minSeparation away from all others
    do {
      x = 5 + Math.random() * 85;  // between 5% and 90%
      y = 5 + Math.random() * 85;
      tries++;
    } while (
      positions.some(pos => dist(pos, {x,y}) < minSeparation) 
      && tries < 20
    );

    // record for future checks
    positions.push({ x, y });

    // build the cloud element
    const cloud = document.createElement("div");
    cloud.className = "cloud";

    // position it
    cloud.style.top  = `${y}%`;
    cloud.style.left = `${x}%`;

    // random scale 1.0–2.0
    const s = (1 + Math.random()).toFixed(2);
    cloud.style.setProperty("--s", s);

    // more powerful float: ±30px to ±60px
    const dx = Math.round(Math.random() * 30 + 30) * (Math.random() < 0.5 ? -1 : 1) + "px";
    const dy = Math.round(Math.random() * 30 + 30) * (Math.random() < 0.5 ? -1 : 1) + "px";
    cloud.style.setProperty("--dx", dx);
    cloud.style.setProperty("--dy", dy);

    // random animation duration 2s–5s
    const dur = (2 + Math.random() * 3).toFixed(2) + "s";
    cloud.style.animationDuration = dur;

    // inject image + label
    cloud.innerHTML = `
      <img src="${cloudSrc}" alt="cloud" class="w-full h-auto" />
      <div class="label">
        ${labels[i % labels.length]}
      </div>
    `;

    container.appendChild(cloud);
  }
});