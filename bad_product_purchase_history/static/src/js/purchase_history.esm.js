/** @odoo-module **/
import {Component, onWillRender} from "@odoo/owl";
import {registry} from "@web/core/registry";
import {usePopover} from "@web/core/popover/popover_hook";
import {useService} from "@web/core/utils/hooks";

export class ProductPurchaseHistoryPopOver extends Component {
    setup() {
        this.actionService = useService("action");
    }

    // Open up a pivot view while clicking on a button(view more ->) located in popover #T6893.
    openPurchasePivotView() {
        this.actionService.doAction(
            "bad_product_purchase_history.action_purchase_order_history",
            {
                additionalContext: {
                    search_default_product_id: this.props.record.data.product_id[0],
                    search_default_group_partner_id: true,
                },
            }
        );
    }
}

ProductPurchaseHistoryPopOver.template =
    "bad_product_purchase_history.ProductPurchaseHistoryPopOver";

export class ProductPurchaseHistoryWidget extends Component {
    setup() {
        this.popover = usePopover(this.constructor.components.Popover, {
            position: "left",
        });
        this.purchaseData = [];
        this.orm = useService("orm");
        onWillRender(() => {
            this.updatePurchaseData();
        });
    }

    // Add the product purchase information #T6893.
    async updatePurchaseData() {
        this.purchaseData = await this.orm.call(
            "purchase.order.line",
            "purchase_order_history",
            [this.props.record.resId],
            {}
        );
    }

    // Show the pop up when click on the widget icon #T6893.
    showPopup(ev) {
        this.popover.open(ev.currentTarget, {
            record: this.props.record,
            purchaseData: this.purchaseData,
        });
    }
}

ProductPurchaseHistoryWidget.components = {Popover: ProductPurchaseHistoryPopOver};
ProductPurchaseHistoryWidget.template =
    "bad_product_purchase_history.ProductPurchaseHistory";

export const productPurchaseHistoryWidget = {
    component: ProductPurchaseHistoryWidget,
};
registry
    .category("view_widgets")
    .add("bad_product_purchase_history_widget", productPurchaseHistoryWidget);
