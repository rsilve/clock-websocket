import {createContext, Dispatch} from "react";
import {IAction} from "./lib/reducer";

export default createContext(null as Dispatch<IAction> | null);
