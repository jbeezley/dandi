(async function () {
    'use strict';

    const attributes = JSON.parse($('#attributes').text())
    const facets = [];

    function createFacet() {
        const facet = $('#facet').val();
        facets.push(facet);
        $('#facetsList').text(facets.join(' / '));
        $(`#facet > option[value=${facet}]`).remove()
        $(`#tree li[data-level="${facets.length - 1}"] .count`).text('');
        if (!$('#facet > option').length) {
            $('#facetForm').remove();
        }
        $('#tree .leaf').each((index, el) => replaceLeafWithFacet(el, facet));
    }

    async function fetchFacets(query, facet) {
        const data = {
            facet: facet
        };
        if (query) {
            data['query'] = query;
        }
        const resp = await fetch(`/api/datasets/facet/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': window.csrfToken
            },
            body: JSON.stringify(data)
        })
        return resp.json();
    }

    async function fetchLeaf(query) {
        let params = '';
        if (query) {
            params = '?' + $.param({query: query});
        }

        const resp = await fetch(`/api/datasets/${params}`)
        return resp.json();
    }

    async function clickLink(evt) {
        const $el = $(evt.currentTarget).parents('li:first');
        evt.preventDefault();
        const level = parseInt($el.data('level'), 10);
        if (level < facets.length) {
            $el.find('a').replaceWith($el.find('a').text());
            expandFacet($el[0], facets[level]);
        } else {
            expandLeaf($el[0]);            
        }
    }

    function fillLeaf(el, data) {
        const $el = $(el);
        const link = $el.find('a');
        link.replaceWith(link.text());
        $el.addClass('leaf');

        $el.find('.count').text(`(${data.count})`);
        const items = filesItems(data);
        $el.append(`<ul>${items}</ul>`);
    }

    function filesItems(data) {
        let items = data.results.map(result => `<li><a href="/datasets/${result.id}/" target="_blank">${result.path}</a></li>`).join('');
        const remain = data.count - data.results.length;
        if (remain > 0) {
            items = items + `<li>... + ${remain} more</li>`;
        }
        return items;
    }

    async function replaceLeafWithFacet(el, facet) {
        const $el = $(el);

        $el.removeClass('leaf');
        $el.find('ul').remove();
        $el.find('.count').text('');

        expandFacet(el, facet);
    }

    async function expandFacet(el, facet) {
        const $el = $(el);
        const query = $el.data('query').trim();
        const level = parseInt($el.data('level'), 10);
        const spinner = $('<div class="spinner"></div>').appendTo(el);

        const data = await fetchFacets(query, facet);
        spinner.remove();
        const remain = data.count - data.results.length;

        let items = data.results.map(result => {
            let subQuery = `${facet} = '${result.facet}'`;
            if (query.length) {
                subQuery = query + ' and ' + subQuery;
            }
            return `
                <li class="folder" data-level="${level + 1}" data-query="${subQuery}">
                    <span>
                        <a class="node" href="#">${result.facet}/</a>
                        <span class="count">(${result.count})</span>
                    </span>
                </li>`
        }).join('');
        if (remain > 0) {
            items = items + `<li>... + ${remain} more</li>`;
        }

        let subQuery = `${facet} = null`;
        if (query) {
            subQuery = query + ' and ' + subQuery;
        }
        const filesData = await fetchLeaf(subQuery);

        items = items + filesItems(filesData);

        $el.find('.count').text(`(${data.count + filesData.count})`);
        $el.append('<ul>' + items + '</ul>');
    }

    async function expandLeaf(el) {
        const $el = $(el);
        const query = $el.data('query');
        const spinner = $('<div class="spinner"></div>').appendTo(el);
        const data = await fetchLeaf(query);
        spinner.remove();
        fillLeaf(el, data);
    }

    const resp = await fetch('/api/datasets/');
    const data = await resp.json();
    fillLeaf($('.root')[0], data);

    $('#createFacet').click(createFacet);
    $('#tree').on('click', 'a.node', clickLink);

})()
