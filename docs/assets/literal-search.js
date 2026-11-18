// 分かち書きで拾えない複合語は、同じMkDocs索引の本文から文字列で探す。
(() => {
  const field = document.querySelector('[data-md-component="search-query"]');
  const native = document.querySelector('[data-md-component="search-result"]');
  if (!field || !native) return;
  const nativeList = native.querySelector("ol");
  const fallback = document.createElement("div");
  fallback.className = "md-search-result";
  fallback.hidden = true;
  native.after(fallback);
  const root = new URL(JSON.parse(document.getElementById("__config").textContent).base + "/", location.href);
  const normalize = value => value.normalize("NFKC").toLocaleLowerCase("ja").trim();
  let entries;
  let timer;
  let run = 0;

  function readIndex() {
    if (!entries) {
      entries = fetch(new URL("search/search_index.json", root))
        .then(response => {
          if (!response.ok) throw new Error("検索索引を読めません");
          return response.json();
        })
        .then(index => index.docs.map(doc => {
          const text = new DOMParser().parseFromString(doc.text, "text/html").body.textContent;
          return { ...doc, text, normalized: normalize(doc.title + " " + text) };
        }))
        .catch(error => { entries = undefined; throw error; });
    }
    return entries;
  }

  async function render(id) {
    const query = normalize(field.value);
    const words = query.split(/\s+/u);
    if (!query || nativeList.childElementCount) return;
    let docs;
    try { docs = await readIndex(); } catch { return; }
    if (id !== run || nativeList.childElementCount) return;
    const matches = docs.filter(doc => words.every(word => doc.normalized.includes(word)));
    if (!matches.length) return;
    const meta = document.createElement("div");
    meta.className = "md-search-result__meta";
    meta.textContent = "本文に一致する項目 " + matches.length + "件";
    const list = document.createElement("ol");
    list.className = "md-search-result__list";
    for (const doc of matches) {
      const li = document.createElement("li");
      li.className = "md-search-result__item";
      const a = document.createElement("a");
      a.className = "md-search-result__link";
      a.href = new URL(doc.location, root).href;
      const title = document.createElement("strong");
      title.textContent = doc.title;
      const excerpt = document.createElement("p");
      const start = Math.max(0, normalize(doc.text).indexOf(words[0]) - 20);
      excerpt.textContent = (start ? "…" : "") + doc.text.slice(start, start + 100);
      a.append(title, excerpt);
      li.append(a);
      list.append(li);
    }
    fallback.replaceChildren(meta, list);
    native.hidden = true;
    fallback.hidden = false;
  }

  function update() {
    clearTimeout(timer);
    const id = ++run;
    fallback.hidden = true;
    native.hidden = false;
    timer = setTimeout(() => render(id), 180);
  }
  field.addEventListener("input", update);
  new MutationObserver(update).observe(nativeList, {childList: true});
})();
