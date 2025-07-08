import { registerGui } from "@point_of_sale/app/utils/registry";
import { MyPopup } from "./MyPopup";
import { PopupButton } from "./PopupButton";

// Register the popup so it can be called
registerGui({
    component: MyPopup,
    name: "MyPopup",
});

// Register the button
registerGui({
    component: PopupButton,
    name: "PopupButton",
    position: "left", // left/right of POS screen
});