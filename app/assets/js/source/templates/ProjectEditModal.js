<div id="{{=kind}}-editor" class="pre-modal" style="opacity: 0;" data-title="editing {{=kind}} ...">
    <form id="{{=kind}}-editor-form">
        {{>fields}}
            {{=name}}:<br>{{+Input}}<br>
        {{/fields}}
        {{>areas}}
            {{=name}}:<br>{{+TextArea}}<br>
        {{/areas}}
        <button id="{{=kind}}-save">save {{=kind}}</button>
    </form>
</div>