class Big3Common {
         
    //bootstrap ��� ����
    static ModalAlert(Bootstrap, ModalId, Option) {

        const OpenModal = new Bootstrap.Modal(document.getElementById(`${ModalId}`), {});
        OpenModal.show();
        return false;
    }
    //bootstrap ��� Close
    static ModalClose(Bootstrap, ModalId,) {
        var CloseModal = document.getElementById(`${ModalId}`);
        var modal = Bootstrap.Modal.getInstance(CloseModal) // Returns a Bootstrap modal instance
        modal.hide();
        return false;
    }
    //Web Api Get �޼ҵ� ȣ��
    static async Get(uri) {
        try {
            const response = await fetch(uri);
            const result = await response.json();
            return result;
        }
        catch (e) {
            console.log("Get==>", e);
        }
    }
    //Web Api Post �޼ҵ� ȣ�� 
    static async Post(uri, jsonObject, toLowerCase = false) {
        try {

            let StringJson = JSON.stringify(jsonObject);
            if (toLowerCase === true) {
                let JsonObj = JSON.parse(StringJson, function (prop, value) {
                    var lower = prop.toLowerCase();
                    if (prop === lower) return value;
                    else this[lower] = value;
                });
                StringJson = JSON.stringify(JsonObj);
            }

            const response = await fetch(uri, {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: StringJson
            });
            const result = await response.json();
            return result;
        }
        catch (e) {
            console.log("Post==>", e);
        }
    }
          
    static Util = {
        
        //Json Ư�� �÷��ǿ��� Ư�� �׸��� ����
        RemoveModelListRow: function (Modelist, DeleteKey, DeleteValue) {
            let idx = Modelist.findIndex((element) => (element[DeleteKey] === DeleteValue));
            if (idx !== -1) {
                Modelist.splice(idx, 1);
            }
            Big3Common.LifeState.ModelUpDate = true;
            return Modelist;
        },
        LabelArray: function (fromdate, todate) {
            const fromdateTime = `${fromdate} 00:00`;
            const todateTime = `${todate} 23:59`;
            const startDate = new Date(fromdateTime);
            const endDate = new Date(todateTime);
            // �迭 �ʱ�ȭ
            let dateArray = [];

            // �����Ϻ��� �����ϱ��� �ݺ�
            for (var currentDate = startDate; currentDate <= endDate; currentDate.setHours(currentDate.getHours() + 1)) {
                let month = String(currentDate.getMonth() + 1).padStart(2, '0');
                let day = String(currentDate.getDate()).padStart(2, '0');
                let hour = String(currentDate.getHours()).padStart(2, '0');
                let formattedDate = month + '.' + day + ' ' + hour;
                dateArray.push(formattedDate);
            }
            return dateArray;
        },
        DataGridGen: function (DataList, coldate,coltemp,colhum) {
            let Table = "";
            let rows = "";
            if (DataList.length === 0) return "";

            DataList.map((list, idx) => {
                const timestamp = list[coldate];
                const date = new Date(timestamp);
                const year = date.getFullYear();
                const month = String(date.getMonth() + 1).padStart(2, '0'); 
                const dateformat = `${year}-${month}`;
                if (idx % 2 == 0) {
                    rows = "<tr>"
                    rows += `<td>${list[coltemp]}</td>`
                    rows += `<td>${dateformat}</td>`
                    rows += `<td>${list[colhum] }</td>`
                }
                else {
                    rows += `<td>${list[coltemp]}</td>`
                    rows += `<td>${dateformat}</td>`
                    rows += `<td>${list[colhum]}</td>`
                    rows += "</tr>";
                    Table += rows;
                    rows = "";
                }
            });
            //������ ���� ������
            if (DataList.length % 2 !== 0) {
                rows += `<td>-</td>`
                rows += `<td>-</td>`
                rows += `<td>-</td>`
                rows += "</tr>";
                Table += rows;
                rows = "";
            }
            return Table;
        },
        LoadingOn: function () {

            const body = document.querySelector("body");
            const myLoading = document.getElementById("myLoading");
            if (myLoading === null) {
                const newDiv = document.createElement("div");
                newDiv.id = "myLoading";
                newDiv.classList.add("loading_wrap");
                let Loading = "";
                Loading += "<div class='dot-wave'>";
                Loading += "<div class='dot-wave__dot'></div>";
                Loading += "<div class='dot-wave__dot'></div>";
                Loading += "<div class='dot-wave__dot'></div>";
                Loading += "<div class='dot-wave__dot'></div>";
                Loading += "</div>";

                newDiv.innerHTML = Loading;
                body.appendChild(newDiv);
            }
            return false;
        },
        LoadingOff: function () {
            const myLoading = document.querySelector("#myLoading");
            if (myLoading !== null) {
                myLoading.remove();
            }
            return false;
        }
    }

}
