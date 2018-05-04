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
      iconClass: 'jp-MaterialIcon jp-ImageIcon',
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
