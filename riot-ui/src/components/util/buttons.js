import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faEdit} from "@fortawesome/free-solid-svg-icons/faEdit";
import Button from "react-bootstrap/Button";
import React from "react";
import {faSync} from "@fortawesome/free-solid-svg-icons/faSync";
import {faTrash} from "@fortawesome/free-solid-svg-icons/faTrash";
import {faPlus} from "@fortawesome/free-solid-svg-icons/faPlus";
import Tooltip from "react-bootstrap/Tooltip";
import OverlayTrigger from "react-bootstrap/OverlayTrigger";
import {faInbox} from "@fortawesome/free-solid-svg-icons/faInbox";
import {faCogs} from "@fortawesome/free-solid-svg-icons/faCogs";
import {InProgressSpinner} from "./util";


export function ToolTipButton(props) {
    return <OverlayTrigger
        placement="top"
        overlay={
            <Tooltip id="">
                {props.tooltip}
            </Tooltip>
        }>
        <Button {...props}>{props.children}</Button>
    </OverlayTrigger>

}

export function MessagesButton(props) {
    return <ToolTipButton
        tooltip="Üzenetek"
        size="sm" variant="outline-primary" {...props}
    ><FontAwesomeIcon icon={faInbox}/></ToolTipButton>
}

export function RulesButton(props) {
    return <ToolTipButton
        tooltip={`Szabályok(${props.count})`}
        size="sm" variant="outline-info" {...props}
    ><FontAwesomeIcon icon={faCogs}/> ({props.count})</ToolTipButton>
}

export function EditButton(props) {
    return <ToolTipButton
        tooltip="Szerkesztés"
        size="sm" variant="outline-secondary" {...props}
    ><FontAwesomeIcon icon={faEdit}/></ToolTipButton>
}

export function DeleteButton(props) {
    return <ToolTipButton
        tooltip="Törlés"
        size="sm" variant="outline-danger" {...props}><FontAwesomeIcon icon={faTrash}/></ToolTipButton>
}

export function AddButton(props) {
    return <ToolTipButton
        tooltip="Hozzáadás"
        variant="success" {...props}><FontAwesomeIcon icon={faPlus}/></ToolTipButton>
}

export function RefreshButton(props) {
    return <ToolTipButton
        tooltip="Frissítés"
        variant="primary" {...props}>
        {props.isLoading ?
            <InProgressSpinner/> :
            <FontAwesomeIcon icon={faSync}/>
        }
    </ToolTipButton>

}