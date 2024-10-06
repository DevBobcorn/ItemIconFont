function tooltipFollow(e, el) {
	x = e.clientX;
	y = e.clientY;
	var tooltip = document.getElementById("tooltip");
	tooltip.innerHTML = el.dataset.tooltip;
	tooltip.style = `top: ${y}px; left: ${x}px;`;
}

function tooltipHide() {
	document.getElementById("tooltip").style = "display: none";
}

function copyText(text) {
	navigator.clipboard.writeText(text);
	var tooltip = document.getElementById("tooltip");
	tooltip.innerHTML = "Copied!";
}

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
                            <span class="cell-glyph underline" data-tooltip="Click to copy character" onmousemove="tooltipFollow(event, this)" onmouseout="tooltipHide()" onclick="copyText('\\u${info.code}')" border="0" style="background-position: -${info.x}px -${info.y}px;">
                        </div>
                        <p class="cell-code underline" data-tooltip="Click to copy escape string" onmousemove="tooltipFollow(event, this)" onmouseout="tooltipHide()" onclick="copyText('\\\\u${info.code}')"><strong>U+${info.code.toUpperCase()}</strong><br>\\u${info.code}</p>
                        <p class="cell-desc" data-tooltip="${info.desc}" onmousemove="tooltipFollow(event, this)" onmouseout="tooltipHide()">${info.desc}</p>`;
        
        if (add_ver !== undefined) {
            newCell.innerHTML +=
                `<p class="cell-version" data-tooltip="Added in ${add_ver}" onmousemove="tooltipFollow(event, this)" onmouseout="tooltipHide()">${add_ver.toUpperCase()}</p>`;
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