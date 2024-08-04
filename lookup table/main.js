function refreshGlyphList(dictText) {
    var container = document.querySelector("#item_container");
    var dict = JSON.parse(dictText);

    for (let key in dict) {
        const newCell = document.createElement("span");
        newCell.classList.add("cell");

        var info = dict[key];
        var add_ver = info.added_in;

        newCell.innerHTML = `
                        <div class="cell-glyph-frame">
                            <span class="cell-glyph underline" title="Click to copy" onclick="navigator.clipboard.writeText('\\u${info.code}')" border="0" style="background-position: -${info.x}px -${info.y}px;">
                        </div>
                        <p class="cell-code underline" title="Click to copy" onclick="navigator.clipboard.writeText('\\\\u${info.code}')"><strong>U+${info.code.toUpperCase()}</strong><br>\\u${info.code}</p>
                        <p class="cell-desc" title="${info.desc}">${info.desc}</p>`;
        
        if (add_ver !== undefined) {
            newCell.innerHTML +=
                `<p class="cell-version" title="Added in ${add_ver}">${add_ver.toUpperCase()}</p>`;
        }

        container.appendChild(newCell);
    }
}

fetch('../mc_atlas_dict_v2.json')
    .then(function(response) {
        return response.text()
    })
    .then(function(glyphDictText) {
        console.log("Glyph dict loaded");
        refreshGlyphList(glyphDictText);
    });