/** @odoo-module **/
import {Component, onWillRender} from "@odoo/owl";
import {registry} from "@web/core/registry";
import {usePopover} from "@web/core/popover/popover_hook";
import {useService} from "@web/core/utils/hooks";

export class ProductSaleHistoryPopOver extends Component {
    setup() {
        this.actionService = useService("action");
    }

    // Open up a pivot view while clicking on a button(view more ->) located in popover #T6892.
    openSalePivotView() {
        this.actionService.doAction(
            "bad_product_sale_history.action_sale_order_history",
            {
                additionalContext: {
                    search_default_product_id: this.props.record.data.product_id[0],
                    search_default_Customer: true,
                },
            }
        );
    }
}

ProductSaleHistoryPopOver.template =
    "bad_product_sale_history.ProductSaleHistoryPopOver";

export class ProductSaleHistoryWidget extends Component {
    setup() {
        this.popover = usePopover(this.constructor.components.Popover, {
            position: "left",
        });
        this.saleData = [];
        this.orm = useService("orm");
        onWillRender(() => {
            this.updateSaleData();
        });
    }

    // Add the product sale information #T6892.
    async updateSaleData() {
        this.saleData = await this.orm.call(
            "sale.order.line",
            "sale_order_history",
            [this.props.record.resId],
            {}
        );
    }

    // Show the pop up when click on the widget icon #T6892.
    showPopup(ev) {
        this.popover.open(ev.currentTarget, {
            record: this.props.record,
            saleData: this.saleData,
        });
    }
}

ProductSaleHistoryWidget.components = {Popover: ProductSaleHistoryPopOver};
ProductSaleHistoryWidget.template = "bad_product_sale_history.ProductSaleHistory";

export const productSaleHistoryWidget = {
    component: ProductSaleHistoryWidget,
};
registry
    .category("view_widgets")
    .add("bad_product_sale_history_widget", productSaleHistoryWidget);
