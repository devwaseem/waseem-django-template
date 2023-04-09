import { $byId } from '@frontend/js/utils'
import './toast.scss'

export enum ToastType {
    INFO = 1,
    WARNING,
    ERROR,
    SUCCESS,
}


const toastContainer = $byId("toast-container")
console.log(toastContainer)

const toastTypeClasses = {
    infoSimple: "toast-info-simple",
    warningSimple: "toast-warning-simple",
    successSimple: "toast-success-simple",
    errorSimple: "toast-error-simple"
}

const toastIds = {
    simple: "toast-simple"
}

class Toast {

    private message: string
    private type: ToastType
    private template: HTMLElement | null = null

    constructor(message: string, type: ToastType) {
        this.message = message
        this.type = type
    }

    public showToast(duration: number = 0) {

        //@ts-ignore
        const template = $byId(toastIds.simple)!.content.firstElementChild.cloneNode(true)
        this.template = template
        toastContainer?.appendChild(template)

        const messageNode = template.querySelector("#message")
        messageNode.textContent = this.message

        switch (this.type) {

            case ToastType.INFO: {
                template.classList.add(toastTypeClasses.infoSimple)
                break;
            }
            case ToastType.ERROR: {
                template.classList.add(toastTypeClasses.errorSimple)
                break;
            }
            case ToastType.WARNING: {
                template.classList.add(toastTypeClasses.warningSimple)
                break;
            }
            case ToastType.SUCCESS: {
                template.classList.add(toastTypeClasses.successSimple)
                break;
            }
        }

        setTimeout(() => {
            template.classList.add('toast-show')
        }, 0)


        template.querySelector("#close-button").addEventListener("click", () => {
            this.closeToast()
        })

        if (duration > 0) {
            setTimeout(() => {
                this.closeToast()
            }, duration)
            const progressBar = document.createElement("div")
            template.appendChild(progressBar)
            progressBar.classList.add("toast-progress-bar")
            progressBar.animate([
                { width: "100%" },
                { width: "0%" }
            ], {
                duration: duration
            })
        }


    }

    public closeToast() {
        this.template!.classList.remove('toast-show')
        setTimeout(() => {
            this.template!.remove()
        }, 600);
    }

}


export default Toast
