function ThemBenhNhan() {
    var table = document.getElementsByTagName("table")[0]

    var newRow = table.insertRow(table.rows.length)

    var cel0 = newRow.insertCell(0)
    var cel1 = newRow.insertCell(1)
    var cel2 = newRow.insertCell(2)
    var cel3 = newRow.insertCell(3)
    var cel4 = newRow.insertCell(4)

    cel0.innerHTML += `
        <input type="text" class="form-control" name="ho-ten" required/>
    `
    cel1.innerHTML += `
        <select class="form-control" name="gioi-tinh" required>
            <option value="Nam" selected>Nam</option>
            <option value="Nữ">Nữ</option>
        </select>
    `
    cel2.innerHTML += `
        <input type="number" class="form-control" name="nam-sinh" required/>
    `
    cel3.innerHTML += `
        <input type="text" class="form-control" name="dia-chi" required/>
    `
    cel4.innerHTML += `
        <input type="button" value="Xóa" class="btn btn-danger" onclick="XoaDong(this)"/>
    `
}

function ThemTrieuChungLoaiBenh() {
    var table = document.getElementsByTagName("table")[0]

    var newRow = table.insertRow(table.rows.length)

    var cel0 = newRow.insertCell(0)
    var cel1 = newRow.insertCell(1)
    var cel2 = newRow.insertCell(2)

    cel0.innerHTML += `
        <input type="text" class="form-control" name="trieu-chung" required/>
    `
    cel1.innerHTML += `
        <input type="text" class="form-control" name="loai-benh" required/>
    `
    cel2.innerHTML += `
        <input type="button" value="Xóa" class="btn btn-danger" onclick="XoaDong(this)"/>
    `

    trieuChung.value = ""
    loaiBenh.value = ""

}

function ThemThuoc() {
    var table = document.getElementsByTagName("table")[1]

    var newRow = table.insertRow(table.rows.length)

    var cel0 = newRow.insertCell(0)
    var cel1 = newRow.insertCell(1)
    var cel2 = newRow.insertCell(2)
    var cel3 = newRow.insertCell(3)
    var cel4 = newRow.insertCell(4)


    cel0.innerHTML += `
        <input type="text" class="form-control" name="thuoc" required/>
    `
    cel1.innerHTML += `
        <select class="form-control" name="don-vi" required>
            <option value="Viên" selected>Viên</option>
            <option value="Chai">Chai</option>
        </select>
    `
    cel2.innerHTML += `
        <input type="number" class="form-control" name="so-luong" required/>
    `
    cel3.innerHTML += `
        <input type="text" class="form-control" name="cach-dung" required/>
    `
    cel4.innerHTML += `
           <input type="button" value="Xóa" class="btn btn-danger" onclick="XoaDong(this)"/>
    `

    thuoc.value = soLuong.value= cachDung.value = ""
    donVi.value = "Viên"

}

function XoaDong(btn) {
    var row = btn.parentNode.parentNode;

    row.parentNode.removeChild(row);
}