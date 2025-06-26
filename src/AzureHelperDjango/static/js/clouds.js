document.addEventListener("DOMContentLoaded", () => {
  const container = document.getElementById("cloud-container");
  const cloudSrc = window.CLOUD_SRC;

  const clouds = [
    { label: "Push an image on a container registry", url: "https://learn.microsoft.com/en-us/azure/devops/pipelines/ecosystems/containers/acr-template?view=azure-devops" },
    { label: "Authentication options", url: "https://learn.microsoft.com/en-us/azure/container-registry/container-registry-authentication?tabs=azure-cli" },
    { label: "Data Lake Storage", url: "https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-introduction" },
    { label: "PowerBI", url: "https://learn.microsoft.com/en-us/power-bi/fundamentals/power-bi-service-overview" },
    { label: "MLStudio", url: "https://azure.microsoft.com/fr-fr/products/machine-learning/#Resources" },
    { label: "Security", url: "https://learn.microsoft.com/en-us/azure/security/" },
    { label: "Azure Functions", url: "https://learn.microsoft.com/en-us/search/?terms=Azure%20functions/" },
    { label: "Databricks", url: "https://learn.microsoft.com/en-us/azure/databricks/" }
  ];

  const count = Math.floor(Math.random() * 4) + 5; // 5..8
  const positions = [];
  const minSeparation = 15;

  function dist(a, b) {
    const dx = a.x - b.x;
    const dy = a.y - b.y;
    return Math.sqrt(dx * dx + dy * dy);
  }

  for (let i = 0; i < count; i++) {
    let x, y, tries = 0;

    do {
      x = 5 + Math.random() * 85;
      y = 5 + Math.random() * 85;
      tries++;
    } while (
      positions.some(pos => dist(pos, { x, y }) < minSeparation) &&
      tries < 20
    );

    positions.push({ x, y });

    const cloud = document.createElement("div");
    cloud.className = "cloud";
    cloud.style.top = `${y}%`;
    cloud.style.left = `${x}%`;

    const s = (1 + Math.random()).toFixed(2);
    cloud.style.setProperty("--s", s);

    const dx = Math.round(Math.random() * 30 + 30) * (Math.random() < 0.5 ? -1 : 1) + "px";
    const dy = Math.round(Math.random() * 30 + 30) * (Math.random() < 0.5 ? -1 : 1) + "px";
    cloud.style.setProperty("--dx", dx);
    cloud.style.setProperty("--dy", dy);

    const dur = (2 + Math.random() * 3).toFixed(2) + "s";
    cloud.style.animationDuration = dur;

    // Créer le lien cliquable
    const link = document.createElement("a");
    const current = clouds[i % clouds.length];
    link.href = current.url;
    link.className = "block text-center hover:scale-105 transition-transform duration-300";
    link.innerHTML = `
      <img src="${cloudSrc}" alt="cloud" class="w-full h-auto" />
      <div class="label mt-1 text-sm font-semibold text-gray-700">
        ${current.label}
      </div>
    `;

    cloud.appendChild(link);
    container.appendChild(cloud);
  }
});
