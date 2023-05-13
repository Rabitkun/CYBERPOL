class RestLab{
    static execAjaxSync(data, method, url){
        let result = null;
        $.ajax({
            type: method,
            url: url,
            data: JSON.stringify(data),
            dataType: "json",
            async: false,
            success: function (response) {
                result = response;
            },
            error: function (xhr, status, error) {
                console.log(error);
            }
        });
        return result;
    }
    static execAjaxAsync(data, method, url, func){
        $.ajax({
            type: method,
            url: url,
            data: JSON.stringify(data),
            dataType: "json",
            async: false,
            success: func,
            error: function (xhr, status, error) {
                console.log(error);
            }
        });
    }

    static getReferencesList(){
        let result = this.execAjaxSync(null, "GET", "/get_refs_list_rest/");
        return result;
    }

    static getIconsList(){
        let result = this.execAjaxSync(null, "GET", "/get_icons_list_rest/");
        return result;
    }

    static getNodeInfo(node_id){
        let data = {"id": node_id};
        let result = this.execAjaxSync(data, "GET", "/get_node_info_rest/");
        return result;
    }

    static createCloudNode(title, pos_x, pos_y){
        let data = {"title": title, "pos_x": pos_x, "pos_y": pos_y};
        let result = this.execAjaxSync(data, "POST", "/create_cloud_node_rest/");
        return result;
    }

    static removeCloudNode(id){
        let data = {"id": id};
        let result = this.execAjaxSync(data, "DELETE", "/remove_cloud_node_rest/");
        return result;
    }

    static createVirtualMachine(title, pos_x, pos_y, reference, cpus, ram, eths, icon){
        let data = {
            "title": title, 
            "pos_x": pos_x, 
            "pos_y": pos_y,
            "reference": reference,
            "cpus": cpus,
            "ram": ram,
            "interfaces": eths,
            "icon": icon
        };
        let result = this.execAjaxSync(data, "POST", "/create_vm_by_ref_rest/");
        return result;
    }

    static removeVirtualMachine(id){
        let data = {"id": id};
        let result = this.execAjaxSync(data, "DELETE", "/delete_vm_rest/");
        return result;
    }

    static getVmStatus(id){
        let data = {"id": id};
        let result = this.execAjaxSync(data, "GET", "/get_vm_status_rest/");
        return result;
    }

    static setVncPort(id, port){
        let data = {"id": id, "port": port};
        let result = this.execAjaxSync(data, "POST", "/set_vnc_port_vm_rest/");
        return result;
    }

    static startVm(id){
        let data = {"id": id};
        let func = (response)=>{
            console.log(response)
        }
        this.execAjaxAsync(data, "POST", "/start_vm_rest/", func);
    }
    static stopVm(id){
        let data = {"id": id};
        let func = (response)=>{
            console.log(response)
        }
        this.execAjaxAsync(data, "POST", "/shutdown_vm_rest/", func);
    }
    static forceStopVm(id){
        let data = {"id": id};
        let func = (response)=>{
            console.log(response)
        }
        this.execAjaxAsync(data, "POST", "/forceoff_vm_rest/", func);
    }


}