/** @odoo-module **/

import { _lt } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";
import { Component, useState } from "@odoo/owl";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { ListController } from "@web/views/list/list_controller";

export class AccountJsonUploader extends Component {
    static template = "accounting_app.AccountJsonUploader";
    setup() {
        console.log("AccountJsonUploader" + this.props);
        this.orm = useService("orm");
        this.action = useService("action");
        this.notification = useService("notification");
        this.state = useState({ value: "" });
        
    }

    onJsonClickButton(){
        console.log("Button Clicked")
        // this.trigger("button_clicked");
    }

    async onJsonDataSubmit() {
        const action = await this.orm.call(
            "account.move",
            "create_documents_from_json",
            [this.state.value],
            {
                context: {  ...this.env.searchModel.context },
            }
        );
        this.state.value = "";
        if (action.context && action.context.notifications) {
            for (let [file, msg] of Object.entries(action.context.notifications)) {
                this.notification.add(
                    msg,
                    {
                        title: file,
                        type: "info",
                        sticky: true,
                    }
                );
            }
            delete action.context.notifications;
        }
        this.action.doAction(action);
    }
}


// registry.add('owl.Component', AccountJsonUploader); 

AccountJsonUploader.template = "accounting_app.AccountJsonUploader";
AccountJsonUploader.props = {
    record: { type: Object, optional: true },
    togglerTemplate: { type: String, optional: true },
    btnClass: { type: String, optional: true },
    linkText: { type: String, optional: true },
    slots: { type: Object, optional: true },
    extraContext: { type: Object, optional: true },
};


export class AccountJsonMoveUploadListRenderer extends ListRenderer {
    setup() {
        super.setup();
        console.log("Custom List Renderer")
    }

    
}

AccountJsonMoveUploadListRenderer.components = {
    ...ListRenderer.components,
    AccountJsonUploader,
};



export class AccountJsonMoveListController extends ListController {
    setup() {
        super.setup();
        this.action = useService("action");
    }

    onClickButton(){
        console.log(this.props.context);
        this.action.doAction('accounting_app.action_file_upload_wizard', {
            additionalContext: this.props.context,
        });
        
    }

    
};

AccountJsonMoveListController.components = {
    ...ListController.components,
    AccountJsonUploader,
};

export const AccountJsonMoveUploadListView = {
    ...listView,
    Controller: AccountJsonMoveListController,
    Renderer: AccountJsonMoveUploadListRenderer,
    buttonTemplate: "accounting_app.ListView.Buttons",
};



registry.category("views").add("account_file_uploader_json", AccountJsonMoveUploadListView);
