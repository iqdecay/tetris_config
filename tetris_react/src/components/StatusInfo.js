import React from 'react';
import {withStyles} from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';
import Dialog from '@material-ui/core/Dialog';
import MuiDialogTitle from '@material-ui/core/DialogTitle';
import MuiDialogContent from '@material-ui/core/DialogContent';
import MuiDialogActions from '@material-ui/core/DialogActions';

const DialogContent = withStyles((theme) => ({
    root: {
        padding: theme.spacing(2),
    },
}))(MuiDialogContent);

const DialogActions = withStyles((theme) => ({
    root: {
        margin: 0,
        padding: theme.spacing(1),
    },
}))(MuiDialogActions);

export default function CustomizedDialogs(props) {
    const [open, setOpen] = React.useState(false);

    const handleClickOpen = () => {
        setOpen(true);
    };
    const handleClose = () => {
        setOpen(false);
    };

    const response = props.beacon.lastAckResponse
    return (
        <div>
            <Button variant="outlined" color="primary" onClick={handleClickOpen}>
                See ACK data
            </Button>
            <Dialog onClose={handleClose} aria-labelledby="customized-dialog-title" open={open}>
                <MuiDialogTitle> ACK frame for device "{props.beacon.name}", id {props.id}</MuiDialogTitle>
                <DialogContent dividers>
                    <ul>
                        <li><h2>device : </h2> {response.device}</li>
                        <li><h2>time : </h2> {response.time}</li>
                        <li><h2>downlinkAck : </h2> {String(response.downlinkAck)}</li>
                        <li><h2>infoCode : </h2> {response.infoCode}</li>
                        <li><h2>infoMessage : </h2> {response.infoMessage}</li>
                        <li><h2>downlinkOverUsage : </h2> {String(response.downlinkOverUsage)}</li>
                    </ul>
                </DialogContent>
                <DialogActions>
                    <Button autoFocus onClick={handleClose} color="primary">
                        Ok
                    </Button>
                </DialogActions>
            </Dialog>
        </div>
    );
}
