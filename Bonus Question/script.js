const API_URL = "http://localhost:8000/search";

async function doSearch() {
  const q = document.getElementById("query").value.trim();
  if (!q) return alert("请输入检索文本！");

  const res = await fetch(`${API_URL}?q=${encodeURIComponent(q)}`);
  const data = await res.json();

  // 分词
  document.getElementById("tokens").textContent = data.tokens.join(" | ");
  // 高频词
  document.getElementById("top10").textContent = data.top10
    .map(o => `${o.word} (${o.count})`).join("\n");
  // 类别
  document.getElementById("category").textContent = data.category;
  // 相似新闻
  const simDiv = document.getElementById("similar");
  simDiv.innerHTML = "";
  data.similar.forEach(item => {
    const card = document.createElement("div");
    card.style.border = "1px solid #ddd";
    card.style.padding = "10px";
    card.style.marginBottom = "10px";
    card.innerHTML = `
      <strong>类别：</strong>${item.category} &nbsp;
      <strong>相似度：</strong>${item.score}<br/>
      <p>${item.news}</p>
    `;
    simDiv.appendChild(card);
  });
}
