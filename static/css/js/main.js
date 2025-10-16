// static/js/main.js (dark theme version)
// Add/remove items, recalc totals, preview DANFE
document.addEventListener('DOMContentLoaded', () => {
    const btnAdd = document.getElementById('btnAddItem');
    const btnClear = document.getElementById('btnClearItems');
    const itemsBody = document.getElementById('itemsBody');
    const totalSubEl = document.getElementById('total_sub');
    const totalIcmsEl = document.getElementById('total_icms');
    const totalGeralEl = document.getElementById('total_geral');
    const btnPreview = document.getElementById('btnPreview');

    function formatBRL(v) { return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(v); }

    function recalcular() {
        let sub = 0, icmsTotal = 0;
        itemsBody.querySelectorAll('tr').forEach(row => {
            const q = parseFloat(row.querySelector('.item-qty').value || 0);
            const p = parseFloat(row.querySelector('.item-price').value || 0);
            const ic = parseFloat(row.querySelector('.item-icms').value || 0);
            const subtotal = q * p;
            const icmsVal = subtotal * (ic / 100);
            row.querySelector('.item-subtotal').textContent = formatBRL(subtotal);
            sub += subtotal; icmsTotal += icmsVal;
        });
        totalSubEl.textContent = formatBRL(sub);
        totalIcmsEl.textContent = formatBRL(icmsTotal);
        totalGeralEl.textContent = formatBRL(sub + icmsTotal);
    }

    function addRow(data = {}) {
        const tr = document.createElement('tr');
        tr.innerHTML = `
      <td><input class="form-control form-control-sm item-desc" name="item_descricao[]" value="${data.desc || ''}"></td>
      <td><input class="form-control form-control-sm item-ncm" name="item_ncm[]" value="${data.ncm || ''}"></td>
      <td><input class="form-control form-control-sm item-cfop" name="item_cfop[]" value="${data.cfop || ''}"></td>
      <td><input class="form-control form-control-sm item-qty" name="item_qt[]" type="number" min="0" value="${data.qty || 1}"></td>
      <td><input class="form-control form-control-sm item-un" name="item_un[]" value="${data.un || 'UN'}"></td>
      <td><input class="form-control form-control-sm item-price" name="item_price[]" type="number" step="0.01" min="0" value="${data.price || 0}"></td>
      <td><input class="form-control form-control-sm item-icms" name="item_icms[]" type="number" step="0.01" min="0" value="${data.icms || 0}"></td>
      <td class="align-middle"><span class="item-subtotal">R$ 0,00</span></td>
      <td class="text-center"><button type="button" class="btn btn-sm btn-danger btn-remove">x</button></td>
    `;
        itemsBody.appendChild(tr);

        tr.querySelectorAll('input').forEach(inp => inp.addEventListener('input', recalcular));
        tr.querySelector('.btn-remove').addEventListener('click', () => { tr.remove(); recalcular(); });
        recalcular();
    }

    btnAdd?.addEventListener('click', () => addRow());
    btnClear?.addEventListener('click', () => { itemsBody.innerHTML = ''; addRow(); recalcular(); });

    if (itemsBody.children.length === 0) addRow();

    btnPreview?.addEventListener('click', () => {
        const danfeBody = document.getElementById('danfeBody');
        let html = `<div class="p-3"><h4>DANFE (preview)</h4><hr>`;
        const clientText = document.getElementById('client_id')?.selectedOptions?.[0]?.text || '';
        html += `<p><strong>Cliente:</strong> ${clientText}</p>`;
        html += `<table class="table table-sm table-dark"><thead><tr><th>Desc</th><th>Qtd</th><th>Preço</th><th>Subtotal</th></tr></thead><tbody>`;
        itemsBody.querySelectorAll('tr').forEach(row => {
            const desc = row.querySelector('.item-desc').value;
            const qty = row.querySelector('.item-qty').value;
            const price = parseFloat(row.querySelector('.item-price').value || 0).toFixed(2);
            const subtotal = (parseFloat(qty) * parseFloat(price)).toFixed(2);
            html += `<tr><td>${desc}</td><td>${qty}</td><td>R$ ${price}</td><td>R$ ${subtotal}</td></tr>`;
        });
        html += `</tbody></table></div>`;
        danfeBody.innerHTML = html;
        new bootstrap.Modal(document.getElementById('danfeModal')).show();
    });

});
