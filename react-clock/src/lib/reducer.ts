interface IState {
    mode: string;
    since?: string;
    timestamp?: string;
    to?: string;
}

export interface IAction {
    type: string;
    payload: unknown;
}

export default (state: IState, action: IAction): IState => {
    switch (action.type) {
        case 'ws':
            return action.payload as IState;
        default:
            throw new Error();
    }
}