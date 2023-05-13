class DialogsLab{
    static ACCEPT_DIALOG_RESULT = {
        ACCEPTED:"accepted",
        REJECTED:"rejected"
    }

    static CreateVmDialog ={
        dialog: null,
        node_x: 0,
        node_y: 0,
        _clearSelectInput(select){
            select.innerHTML = "";
        },
        _fillSelectInput(select, data){
            this._clearSelectInput(select);
            for (var key in data){
                var option = document.createElement('option')
                option.setAttribute("value", key.toString());
                option.text = data[key];
                select.appendChild(option);
            }
            //select.setAttribute("value", data)
        },
        getTitle(dialog){
            return dialog.getElementsByClassName("create-vm-dialog-input-title")[0].value;
        },
        getRef(dialog){
            var select = dialog.getElementsByClassName("create-vm-dialog-input-reference")[0];
            var selectedOption = select.options[select.selectedIndex];
            var selectedValue = selectedOption.value;
            return selectedValue;
        },
        getIcon(dialog){
            var select = dialog.getElementsByClassName("create-vm-dialog-input-icon")[0];
            var selectedOption = select.options[select.selectedIndex];
            var selectedValue = selectedOption.value;
            return selectedValue;
        },
        getCpus(dialog){
            return dialog.getElementsByClassName("create-vm-dialog-input-cpus")[0].value;
        },
        getRam(dialog){
            return dialog.getElementsByClassName("create-vm-dialog-input-ram")[0].value;
        },
        getInterfaces(dialog){
            return dialog.getElementsByClassName("create-vm-dialog-input-eth")[0].value;
        },
        getParams(dialog){
            var result = new Object();
            result.title = this.getTitle(dialog);
            result.ref = this.getRef(dialog);
            result.icon = this.getIcon(dialog);
            result.cpus = this.getCpus(dialog);
            result.ram = this.getRam(dialog);
            result.interfaces = this.getInterfaces(dialog);
            return result;
        },
        _onAccept(event){
            var params = this.getParams(this.dialog);
            console.log(params);
            var result = RestLab.createVirtualMachine(
                params.title,
                this.node_x,
                this.node_y,
                params.ref,
                params.cpus,
                params.ram,
                params.interfaces,
                params.icon
            );
            console.log(result)

            this.dialog.close();
            if (result["status"] != "success")
                return;
            LabField.addNode(
                document.body,
                result["id"],
                params.title,
                this.node_x,
                this.node_y,
                params.icon
            );
        },
        _onCancel(event){
            this.dialog.close();
        },
        openCreateVmDialog(node_x, node_y){
            this.dialog = document.getElementById("create-vm-dialog");
            this.node_x = node_x;
            this.node_y = node_y;

            var refs_element = this.dialog.getElementsByClassName("create-vm-dialog-input-reference")[0];
            this._fillSelectInput(refs_element, RestLab.getReferencesList());
            var icons_element = this.dialog.getElementsByClassName("create-vm-dialog-input-icon")[0];
            this._fillSelectInput(icons_element, RestLab.getIconsList());
            
            var btn_create = this.dialog.getElementsByClassName("labdialog__button-create")[0];
            var btn_cancel = this.dialog.getElementsByClassName("labdialog__button-cancel")[0];
            console.log("x:", this.node_x, "y:", this.node_y);
            this.dialog.showModal();
        },
    }


    static generateAcceptDialog(message){
        let dialog = document.createElement("dialog")
        let dialog_title = document.createElement('span')
        let inner_form = document.createElement("form")
        let accept_btn = document.createElement('button')
        let reject_btn = document.createElement('button')
        
        dialog.setAttribute("id", "accept-dialog")
        dialog.classList.add("dialog__accept")
    
        dialog_title.textContent = message
        dialog_title.setAttribute('id', "accept-dialog-title")
        dialog_title.classList.add("dialog__title")
    
        inner_form.method = "dialog"
    
        accept_btn.value = ACCEPT_DIALOG_RESULT.ACCEPTED
        accept_btn.textContent = "Подтвердить"
        accept_btn.classList.add("btn__accept")
    
        reject_btn.value = ACCEPT_DIALOG_RESULT.REJECTED
        reject_btn.textContent = "Отмена"
        reject_btn.classList.add("btn__reject")
    
        dialog.appendChild(dialog_title)
        dialog.appendChild(inner_form)
        inner_form.appendChild(accept_btn)
        inner_form.appendChild(reject_btn)
        document.body.appendChild(dialog)
        return dialog
    }
    
}
class DialogsLabListeners{

}