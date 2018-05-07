import {
  JupyterLab, JupyterLabPlugin, ILayoutRestorer
} from '@jupyterlab/application';

import {
  ICommandPalette, showDialog, Dialog
} from '@jupyterlab/apputils';

import {
  IDocumentManager
} from '@jupyterlab/docmanager';

import {
  IFileBrowserFactory
} from '@jupyterlab/filebrowser';

import {
  ILauncher
} from '@jupyterlab/launcher';

import {
  IMainMenu
} from '@jupyterlab/mainmenu';

import {
  Widget
} from '@phosphor/widgets';

import '../style/index.css';

const extension: JupyterLabPlugin<void> = {
  id: 'jupyterlab_templates',
  autoStart: true,
  requires: [IDocumentManager, ICommandPalette, ILayoutRestorer, IMainMenu, IFileBrowserFactory],
  optional: [ILauncher],
  activate: activate
};


var templates: Array<String>;



class OpenTemplateWidget extends Widget {
  constructor() {
    let body = document.createElement('div');
    let label = document.createElement('label');
    label.textContent = 'From Template:';

    let input = document.createElement('select');
    for(let t of templates){
      let val = document.createElement('option');
      val.label = t[0];
      val.text  = t[0];
      val.value = t[2];
      input.appendChild(val);
    }

    input.placeholder = 'select';

    body.appendChild(label);
    body.appendChild(input);
    super({ node: body });
  }

  getValue(): string {
    return this.inputNode.value;
  }

  get inputNode(): HTMLSelectElement {
    return this.node.getElementsByTagName('select')[0] as HTMLSelectElement;
  }
}

function newFromTemplate(app: JupyterLab, browser: IFileBrowserFactory): Promise<Widget> {
  return new Promise(function(resolve){
    showDialog({
        title: 'From Template',
        body: new OpenTemplateWidget(),
        focusNodeSelector: 'input',
        buttons: [Dialog.cancelButton(), Dialog.okButton({ label: 'GO' })]
      }).then(result => {
        if (result.button.label === 'CANCEL') {
          return;
        }
        let path = browser.defaultBrowser.model.path;
        app.commands.execute(
          'docmanager:new-untitled', {path: path, type: 'notebook' }
        ).then((model) => {
          app.commands.execute('docmanager:open', {
            path: model.path, factory: 'Notebook'
          }).then(widget=> {
              widget.context.ready.then(() =>{
                widget.model.fromString(result.value);
                resolve(widget);
              });
          });
        });
      });
    });
}


function activate(app: JupyterLab,
                  docManager: IDocumentManager,
                  palette: ICommandPalette,
                  restorer: ILayoutRestorer,
                  menu: IMainMenu,
                  browser: IFileBrowserFactory,
                  launcher: ILauncher | null) {

  // grab templates from serverextension
  var xhr = new XMLHttpRequest();
  xhr.open("GET", "/templates/get", true);
  xhr.onload = function (e:any) {
    if (xhr.readyState === 4) {
      if (xhr.status === 200) {
        let sites = JSON.parse(xhr.responseText);
        templates = sites;
      } else {
        console.error(xhr.statusText);
      }
    }
  }.bind(this);
  xhr.onerror = function (e) {
    console.error(xhr.statusText);
  };
  xhr.send(null);

  // Add an application command
  const open_command = 'template:open';

  app.commands.addCommand(open_command, {
    label: 'From Template',
    isEnabled: () => true,
    execute: args => {
      showDialog({
          title: 'From Template',
          body: new OpenTemplateWidget(),
          focusNodeSelector: 'input',
          buttons: [Dialog.cancelButton(), Dialog.okButton({ label: 'GO' })]
        }).then(result => {
          if (result.button.label === 'CANCEL') {
            return;
          }

          let path = browser.defaultBrowser.model.path;
          
          return new Promise(function(resolve) {
            app.commands.execute(
            'docmanager:new-untitled', {path: path, type: 'notebook' }
          ).then((model) => {
            app.commands.execute('docmanager:open', {
              path: model.path, factory: 'Notebook'
            }).then(widget=> {
              widget.context.ready.then(() =>{
                widget.model.fromString(result.value);
                resolve(widget);
              });
            });
          });
        });
        });
      }
    });


  // Add a launcher item if the launcher is available.
  if (launcher) {
    launcher.add({
      displayName: 'From Template',
      name: 'template',
      iconClass: 'jp-TemplateIcon',
      kernelIconUrl: 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 203 226"><defs><style>.cls-1{fill:#ff780a;}.cls-2,.cls-3{fill:#fff;}.cls-3{font-size:6px;font-family:MyriadPro-Regular, Myriad Pro;letter-spacing:0.01em;}.cls-4{letter-spacing:0em;}.cls-5{fill:#3fa9f5;}.cls-6{fill:#7ac943;}.cls-7{fill:#ff931e;}.cls-8{fill:#ff7bac;}.cls-10,.cls-9{fill:none;stroke-miterlimit:10;}.cls-9{stroke:#ff1d25;}.cls-10{stroke:#000;stroke-width:2px;}.cls-11{font-size:26px;font-family:HelveticaNeue-Italic, Helvetica Neue;font-style:italic;}.cls-12{letter-spacing:-0.09em;}</style></defs><title>Asset 3</title><g id="Layer_2" data-name="Layer 2"><g id="Layer_1-2" data-name="Layer 1"><rect class="cls-1" x="0.5" y="0.5" width="202" height="225"/><path d="M202,1V225H1V1H202m1-1H0V226H203V0Z"/><rect class="cls-2" x="32.5" y="15.5" width="137" height="32"/><path d="M169,16V47H33V16H169m1-1H32V48H170V15Z"/><text class="cls-3" transform="translate(11.33 23.33)">I<tspan class="cls-4" x="1.49" y="0">n [1]:</tspan></text><text class="cls-3" transform="translate(11.33 65.33)">I<tspan class="cls-4" x="1.49" y="0">n [2]:</tspan></text><rect class="cls-2" x="19.5" y="104" width="160" height="103.48"/><path d="M179,104.5V207H20V104.5H179m1-1H19V208H180V103.5Z"/><rect class="cls-5" x="38.7" y="179.72" width="13.7" height="22.27"/><rect class="cls-6" x="74.66" y="150.6" width="13.7" height="51.38"/><rect class="cls-7" x="110.63" y="159.16" width="13.7" height="42.82"/><rect class="cls-8" x="146.6" y="136.9" width="13.7" height="65.09"/><line class="cls-9" x1="45.55" y1="169.44" x2="81.52" y2="119.77"/><line class="cls-9" x1="117.48" y1="140.32" x2="81.52" y2="119.77"/><line class="cls-9" x1="153.45" y1="109.49" x2="117.48" y2="140.32"/><rect class="cls-2" x="32.5" y="58.5" width="137" height="36"/><path d="M169,59V94H33V59H169m1-1H32V95H170V58Z"/><line class="cls-10" x1="40.5" y1="62.55" x2="71" y2="62.55"/><line class="cls-10" x1="41" y1="68.31" x2="90" y2="68.31"/><line class="cls-10" x1="41" y1="74.38" x2="152" y2="74.38"/><line class="cls-10" x1="41" y1="80.44" x2="152" y2="80.44"/><line class="cls-10" x1="41" y1="86.51" x2="90" y2="86.51"/><text class="cls-11" transform="translate(34.75 41)">TEMPL<tspan class="cls-12" x="84.73" y="0">A</tspan><tspan x="99.68" y="0">TE</tspan></text></g></g></svg>',

      callback: () => {return newFromTemplate(app, browser);},
      rank: 1,
      category: 'Notebook'
    });
  }

  if (menu) {
    // Add new text file creation to the file menu.
    menu.fileMenu.newMenu.addGroup([{ command: open_command }], 40);
  }

  console.log('JupyterLab extension jupyterlab_templates is activated!');
};


export default extension;
