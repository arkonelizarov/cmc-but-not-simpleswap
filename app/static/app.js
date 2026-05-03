const searchInput = document.querySelector("#coin-search");
const visibleCount = document.querySelector("#visible-count");
const emptyState = document.querySelector("#empty-state");
const rows = Array.from(document.querySelectorAll("#coin-table tr"));

function applyFilter() {
    const query = searchInput.value.trim().toUpperCase();
    let matches = 0;

    rows.forEach((row) => {
        const symbol = row.dataset.symbol || "";
        const isMatch = symbol.includes(query);
        row.hidden = !isMatch;
        if (isMatch) {
            matches += 1;
        }
    });

    visibleCount.textContent = matches.toLocaleString();
    emptyState.hidden = matches > 0;
}

if (searchInput) {
    searchInput.addEventListener("input", applyFilter);
}
