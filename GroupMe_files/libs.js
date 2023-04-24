/*! For license information please see libs.js.LICENSE.txt */
    <span
        part="end"
        ${wt("endContainer")}
        class=${e=>t.end?"end":void 0}
    >
        <slot name="end" ${wt("end")} @slotchange="${e=>e.handleEndContentChange()}">
            ${t.end||""}
        </slot>
    </span>
`,kt=(e,t)=>_t`
    <span
        part="start"
        ${wt("startContainer")}
        class="${e=>t.start?"start":void 0}"
    >
        <slot
            name="start"
            ${wt("start")}
            @slotchange="${e=>e.handleStartContentChange()}"
        >
            ${t.start||""}
        </slot>
    </span>
`,St=_t`
    <span part="end" ${wt("endContainer")}>
        <slot
            name="end"
            ${wt("end")}
            @slotchange="${e=>e.handleEndContentChange()}"
        ></slot>
    </span>
`,Mt=_t`
    <span part="start" ${wt("startContainer")}>
        <slot
            name="start"
            ${wt("start")}
            @slotchange="${e=>e.handleStartContentChange()}"
        ></slot>
    </span>
  font-family: ${yr};
  font-size: ${_r};
  line-height: ${$r};
  font-weight: initial;
  font-variation-settings: ${wr};
`,Ws=Ht`
  font-family: ${yr};
  font-size: ${xr};
  line-height: ${Tr};
  font-weight: initial;
  font-variation-settings: ${kr};
`,Gs=Ht`
  font-family: ${yr};
  font-size: ${Sr};
  line-height: ${Mr};
  font-weight: initial;
  font-variation-settings: ${Cr};
`,qs=Ht`
  font-family: ${yr};
  font-size: ${Lr};
  line-height: ${Dr};
  font-weight: initial;
  font-variation-settings: ${Er};
`,Ks=Ht`
  font-family: ${yr};
  font-size: ${Ar};
  line-height: ${Nr};
  font-weight: initial;
  font-variation-settings: ${Or};
`,Js=Ht`
  font-family: ${yr};
  font-size: ${Pr};
  line-height: ${Ir};
  font-weight: initial;
  font-variation-settings: ${Rr};
`,Xs=Ht`
  font-family: ${yr};
  font-size: ${Fr};
  line-height: ${Yr};
  font-weight: initial;
  font-variation-settings: ${jr};
`,Zs=Ht`
  font-family: ${yr};
  font-size: ${Hr};
  line-height: ${Ur};
  font-weight: initial;
  font-variation-settings: ${Br};
`,Qs=Ht`
  font-family: ${yr};
  font-size: ${Vr};
  line-height: ${zr};
  font-weight: initial;
  font-variation-settings: ${Wr};
`,el=(e,t)=>Yt`
    ${Bt("flex")} :host {
      box-sizing: border-box;
      flex-direction: column;
      ${zs}
      color: ${pa};
      gap: calc(${hr} * 1px);
    }
  `;function tl(){return!("undefined"==typeof window||!window.document||!window.document.createElement)}function nl(...e){return e.every((e=>e instanceof HTMLElement))}let rl;const ol=function(){if("boolean"==typeof rl)return rl;if(!tl())return rl=!1,rl;const e=document.createElement("style"),t=function(){const e=document.querySelector('meta[property="csp-nonce"]');return e?e.getAttribute("content"):null}();null!==t&&e.setAttribute("nonce",t),document.head.appendChild(e);try{e.sheet.insertRule("foo:focus-visible {color:inherit}",0),rl=!0}catch(e){rl=!1}finally{document.head.removeChild(e)}return rl}()?"focus-visible":"focus";class il{constructor(e){this.listenerCache=new WeakMap,this.query=e}bind(e){const{query:t}=this,n=this.constructListener(e);n.bind(t)(),t.addListener(n),this.listenerCache.set(e,n)}unbind(e){const t=this.listenerCache.get(e);t&&(this.query.removeListener(t),this.listenerCache.delete(e))}}class al extends il{constructor(e,t){super(e),this.styles=t}static with(e){return t=>new al(e,t)}constructListener(e){let t=!1;const n=this.styles;return function(){const{matches:r}=this;r&&!t?(e.$fastController.addStyles(n),t=r):!r&&t&&(e.$fastController.removeStyles(n),t=r)}}unbind(e){super.unbind(e),e.$fastController.removeStyles(this.styles)}}const sl=al.with(window.matchMedia("(forced-colors)"));al.with(window.matchMedia("(prefers-color-scheme: dark)")),al.with(window.matchMedia("(prefers-color-scheme: light)"));var ll;!function(e){e.Canvas="Canvas",e.CanvasText="CanvasText",e.LinkText="LinkText",e.VisitedText="VisitedText",e.ActiveText="ActiveText",e.ButtonFace="ButtonFace",e.ButtonText="ButtonText",e.Field="Field",e.FieldText="FieldText",e.Highlight="Highlight",e.HighlightText="HighlightText",e.GrayText="GrayText"}(ll||(ll={}));const ul=Ht`
  outline: calc(${gr} * 1px) solid ${Wa};
  outline-offset: calc(${gr} * -1px);
`,dl=Ht`
  outline: calc(${gr} * 1px) solid ${Wa};
  outline-offset: calc(${mr} * 1px);
`,cl=Ht`(${ur} + ${cr}) * ${hr}`,hl=ln.create("neutral-fill-stealth-rest-on-neutral-fill-layer-rest").withDefault((e=>{const t=zi.getValueFor(e);return na.getValueFor(e).evaluate(e,t.evaluate(e).rest).rest})),pl=ln.create("neutral-fill-stealth-hover-on-neutral-fill-layer-rest").withDefault((e=>{const t=zi.getValueFor(e);return na.getValueFor(e).evaluate(e,t.evaluate(e).rest).hover})),fl=ln.create("neutral-fill-stealth-active-on-neutral-fill-layer-rest").withDefault((e=>{const t=zi.getValueFor(e);return na.getValueFor(e).evaluate(e,t.evaluate(e).rest).active})),ml=(e,t)=>Yt`
    ${Bt("flex")} :host {
      box-sizing: border-box;
      ${zs};
      flex-direction: column;
      background: ${Wi};
      color: ${pa};
      border: calc(${mr} * 1px) solid ${Ra};
      border-radius: calc(${fr} * 1px);
    }

    .region {
      display: none;
      padding: calc(${hr} * 2 * 1px);
      background: ${Ji};
    }

    .heading {
      display: grid;
      position: relative;
      grid-template-columns: auto 1fr auto auto;
      align-items: center;
    }

    .button {
      appearance: none;
      border: none;
      background: none;
      grid-column: 2;
      grid-row: 1;
      outline: none;
      margin: calc(${hr} * 3 * 1px) 0;
      padding: 0 calc(${hr} * 2 * 1px);
      text-align: left;
      color: inherit;
      cursor: pointer;
      font: inherit;
    }

    .button::before {
      content: '';
      position: absolute;
      top: calc(${mr} * -1px);
      left: calc(${mr} * -1px);
      right: calc(${mr} * -1px);
      bottom: calc(${mr} * -1px);
      cursor: pointer;
    }

    .button:${ol}::before {
      ${ul}
      border-radius: calc(${fr} * 1px);
    }

    :host(.expanded) .button:${ol}::before {
      border-bottom-left-radius: 0;
      border-bottom-right-radius: 0;
    }

    :host(.expanded) .region {
      display: block;
      border-top: calc(${mr} * 1px) solid ${Ra};
      border-bottom-left-radius: calc((${fr} - ${mr}) * 1px);
      border-bottom-right-radius: calc((${fr} - ${mr}) * 1px);
    }

    .icon {
      display: flex;
      align-items: center;
      justify-content: center;
      grid-column: 4;
      pointer-events: none;
      background: ${hl};
      border-radius: calc(${pr} * 1px);
      fill: currentcolor;
      width: calc(${cl} * 1px);
      height: calc(${cl} * 1px);
      margin: calc(${hr} * 2 * 1px);
    }

    .heading:hover .icon {
      background: ${pl};
    }

    .heading:active .icon {
      background: ${fl};
    }

    slot[name='collapsed-icon'] {
      display: flex;
    }

    :host(.expanded) slot[name='collapsed-icon'] {
      display: none;
    }

    slot[name='expanded-icon'] {
      display: none;
    }

    :host(.expanded) slot[name='expanded-icon'] {
      display: flex;
    }

    .start {
      display: flex;
      align-items: center;
      padding-inline-start: calc(${hr} * 2 * 1px);
      justify-content: center;
      grid-column: 1;
    }

    .end {
      display: flex;
      align-items: center;
      justify-content: center;
      grid-column: 3;
    }

    .icon,
    .start,
    .end {
      position: relative;
    }
  `.withBehaviors(sl(Yt`
        .button:${ol}::before {
          outline-color: ${ll.Highlight};
        }
        .icon {
          fill: ${ll.ButtonText};
        }
      `)),gl=Lt.compose({baseName:"accordion-item",template:(e,t)=>_t`
    <template class="${e=>e.expanded?"expanded":""}">
        <div
            class="heading"
            part="heading"
            role="heading"
            aria-level="${e=>e.headinglevel}"
        >
            <button
                class="button"
                part="button"
                ${wt("expandbutton")}
                aria-expanded="${e=>e.expanded}"
                aria-controls="${e=>e.id}-panel"
                id="${e=>e.id}"
                @click="${(e,t)=>e.clickHandler(t.event)}"
            >
                <span class="heading-content" part="heading-content">
                    <slot name="heading"></slot>
                </span>
            </button>
            ${kt(0,t)}
            ${Tt(0,t)}
            <span class="icon" part="icon" aria-hidden="true">
                <slot name="expanded-icon" part="expanded-icon">
                    ${t.expandedIcon||""}
                </slot>
                <slot name="collapsed-icon" part="collapsed-icon">
                    ${t.collapsedIcon||""}
                </slot>
            <span>
        </div>
        <div
            class="region"
            part="region"
            id="${e=>e.id}-panel"
            role="region"
            aria-labelledby="${e=>e.id}"
        >
            <slot></slot>
        </div>
    </template>
`,styles:ml,collapsedIcon:'\n    <svg width="12" height="12" xmlns="http://www.w3.org/2000/svg">\n      <path d="M2.15 4.65c.2-.2.5-.2.7 0L6 7.79l3.15-3.14a.5.5 0 11.7.7l-3.5 3.5a.5.5 0 01-.7 0l-3.5-3.5a.5.5 0 010-.7z"/>\n    </svg>\n  ',expandedIcon:'\n    <svg width="12" height="12" xmlns="http://www.w3.org/2000/svg">\n      <path d="M2.15 7.35c.2.2.5.2.7 0L6 4.21l3.15 3.14a.5.5 0 10.7-.7l-3.5-3.5a.5.5 0 00-.7 0l-3.5 3.5a.5.5 0 000 .7z"/>\n    </svg>\n  '}),yl=ml,vl=At.compose({baseName:"accordion",template:(e,t)=>_t`
    <template>
        <slot ${It({property:"accordionItems",filter:Nt()})}></slot>
        <slot name="item" part="item" ${It("accordionItems")}></slot>
    </template>
`,styles:el}),bl=el;function _l(e,t,n,r){var o,i=arguments.length,a=i<3?t:null===r?r=Object.getOwnPropertyDescriptor(t,n):r;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)a=Reflect.decorate(e,t,n,r);else for(var s=e.length-1;s>=0;s--)(o=e[s])&&(a=(i<3?o(a):i>3?o(t,n,a):o(t,n))||a);return i>3&&a&&Object.defineProperty(t,n,a),a}Object.create;Object.create;class $l{}r([M({attribute:"aria-atomic"})],$l.prototype,"ariaAtomic",void 0),r([M({attribute:"aria-busy"})],$l.prototype,"ariaBusy",void 0),r([M({attribute:"aria-controls"})],$l.prototype,"ariaControls",void 0),r([M({attribute:"aria-current"})],$l.prototype,"ariaCurrent",void 0),r([M({attribute:"aria-describedby"})],$l.prototype,"ariaDescribedby",void 0),r([M({attribute:"aria-details"})],$l.prototype,"ariaDetails",void 0),r([M({attribute:"aria-disabled"})],$l.prototype,"ariaDisabled",void 0),r([M({attribute:"aria-errormessage"})],$l.prototype,"ariaErrormessage",void 0),r([M({attribute:"aria-flowto"})],$l.prototype,"ariaFlowto",void 0),r([M({attribute:"aria-haspopup"})],$l.prototype,"ariaHaspopup",void 0),r([M({attribute:"aria-hidden"})],$l.prototype,"ariaHidden",void 0),r([M({attribute:"aria-invalid"})],$l.prototype,"ariaInvalid",void 0),r([M({attribute:"aria-keyshortcuts"})],$l.prototype,"ariaKeyshortcuts",void 0),r([M({attribute:"aria-label"})],$l.prototype,"ariaLabel",void 0),r([M({attribute:"aria-labelledby"})],$l.prototype,"ariaLabelledby",void 0),r([M({attribute:"aria-live"})],$l.prototype,"ariaLive",void 0),r([M({attribute:"aria-owns"})],$l.prototype,"ariaOwns",void 0),r([M({attribute:"aria-relevant"})],$l.prototype,"ariaRelevant",void 0),r([M({attribute:"aria-roledescription"})],$l.prototype,"ariaRoledescription",void 0);class wl extends ze{constructor(){super(...arguments),this.handleUnsupportedDelegatesFocus=()=>{var e;window.ShadowRoot&&!window.ShadowRoot.prototype.hasOwnProperty("delegatesFocus")&&(null===(e=this.$fastController.definition.shadowOptions)||void 0===e?void 0:e.delegatesFocus)&&(this.focus=()=>{this.control.focus()})}}connectedCallback(){super.connectedCallback(),this.handleUnsupportedDelegatesFocus()}}r([M],wl.prototype,"download",void 0),r([M],wl.prototype,"href",void 0),r([M],wl.prototype,"hreflang",void 0),r([M],wl.prototype,"ping",void 0),r([M],wl.prototype,"referrerpolicy",void 0),r([M],wl.prototype,"rel",void 0),r([M],wl.prototype,"target",void 0),r([M],wl.prototype,"type",void 0),r([b],wl.prototype,"defaultSlottedContent",void 0);class xl{}r([M({attribute:"aria-expanded"})],xl.prototype,"ariaExpanded",void 0),Ct(xl,$l),Ct(wl,xt,xl);const Tl=(e,t)=>_t`
    <a
        class="control"
        part="control"
        download="${e=>e.download}"
        href="${e=>e.href}"
        hreflang="${e=>e.hreflang}"
        ping="${e=>e.ping}"
        referrerpolicy="${e=>e.referrerpolicy}"
        rel="${e=>e.rel}"
        target="${e=>e.target}"
        type="${e=>e.type}"
        aria-atomic="${e=>e.ariaAtomic}"
        aria-busy="${e=>e.ariaBusy}"
        aria-controls="${e=>e.ariaControls}"
        aria-current="${e=>e.ariaCurrent}"
        aria-describedby="${e=>e.ariaDescribedby}"
        aria-details="${e=>e.ariaDetails}"
        aria-disabled="${e=>e.ariaDisabled}"
        aria-errormessage="${e=>e.ariaErrormessage}"
        aria-expanded="${e=>e.ariaExpanded}"
        aria-flowto="${e=>e.ariaFlowto}"
        aria-haspopup="${e=>e.ariaHaspopup}"
        aria-hidden="${e=>e.ariaHidden}"
        aria-invalid="${e=>e.ariaInvalid}"
        aria-keyshortcuts="${e=>e.ariaKeyshortcuts}"
        aria-label="${e=>e.ariaLabel}"
        aria-labelledby="${e=>e.ariaLabelledby}"
        aria-live="${e=>e.ariaLive}"
        aria-owns="${e=>e.ariaOwns}"
        aria-relevant="${e=>e.ariaRelevant}"
        aria-roledescription="${e=>e.ariaRoledescription}"
        ${wt("control")}
    >
        ${kt(0,t)}
        <span class="content" part="content">
            <slot ${It("defaultSlottedContent")}></slot>
        </span>
        ${Tt(0,t)}
    </a>
`,kl=(e,t,n,r="[disabled]")=>Yt`
    ${Bt("inline-flex")}
    
    :host {
      position: relative;
      box-sizing: border-box;
      ${zs}
      height: calc(${cl} * 1px);
      min-width: calc(${cl} * 1px);
      color: ${pa};
      border-radius: calc(${pr} * 1px);
      fill: currentcolor;
    }

    .control {
      border: calc(${mr} * 1px) solid transparent;
      flex-grow: 1;
      box-sizing: border-box;
      display: inline-flex;
      justify-content: center;
      align-items: center;
      padding: 0 calc((10 + (${hr} * 2 * ${cr})) * 1px);
      white-space: nowrap;
      outline: none;
      text-decoration: none;
      color: inherit;
      border-radius: inherit;
      fill: inherit;
      font-family: inherit;
    }

    .control,
    .end,
    .start {
      font: inherit;
    }

    .control.icon-only {
      padding: 0;
      line-height: 0;
    }

    .control:${ol} {
      ${ul}
    }

    .control::-moz-focus-inner {
      border: 0;
    }

    .content {
      pointer-events: none;
    }

    .start,
    .end {
      display: flex;
      pointer-events: none;
    }

    .start {
      margin-inline-end: 11px;
    }

    .end {
      margin-inline-start: 11px;
    }
  `,Sl=(e,t,n,r="[disabled]")=>Yt`
    .control {
      background: padding-box linear-gradient(${Ei}, ${Ei}),
        border-box ${ka};
    }

    :host(${n}:hover) .control {
      background: padding-box linear-gradient(${Ai}, ${Ai}),
        border-box ${Sa};
    }

    :host(${n}:active) .control {
      background: padding-box linear-gradient(${Ni}, ${Ni}),
        border-box ${Ma};
    }

    :host(${r}) .control {
      background: padding-box linear-gradient(${Ei}, ${Ei}),
        border-box ${_a};
    }
  `.withBehaviors(sl(Yt`
        .control {
          background: ${ll.ButtonFace};
          border-color: ${ll.ButtonText};
          color: ${ll.ButtonText};
        }

        :host(${n}:hover) .control,
        :host(${n}:active) .control {
          forced-color-adjust: none;
          background: ${ll.HighlightText};
          border-color: ${ll.Highlight};
          color: ${ll.Highlight};
        }

        :host(${r}) .control {
          background: transparent;
          border-color: ${ll.GrayText};
          color: ${ll.GrayText};
        }

        .control:${ol} {
          outline-color: ${ll.CanvasText};
        }

        :host([href]) .control {
          background: transparent;
          border-color: ${ll.LinkText};
          color: ${ll.LinkText};
        }

        :host([href]:hover) .control,
        :host([href]:active) .control {
          background: transparent;
          border-color: ${ll.CanvasText};
          color: ${ll.CanvasText};
        }
    `)),Ml=(e,t,n,r="[disabled]")=>Yt`
    .control {
      background: padding-box linear-gradient(${ci}, ${ci}),
        border-box ${Si};
      color: ${gi};
    }

    :host(${n}:hover) .control {
      background: padding-box linear-gradient(${hi}, ${hi}),
        border-box ${Mi};
      color: ${yi};
    }

    :host(${n}:active) .control {
      background: padding-box linear-gradient(${pi}, ${pi}),
        border-box ${Ci};
      color: ${vi};
    }

    :host(${r}) .control {
      background: ${ci};
    }

    .control:${ol} {
      box-shadow: 0 0 0 calc(${gr} * 1px) ${qa} inset !important;
    }
  `.withBehaviors(sl(Yt`
        .control {
          forced-color-adjust: none;
          background: ${ll.Highlight};
          color: ${ll.HighlightText};
        }

        :host(${n}:hover) .control,
        :host(${n}:active) .control {
          background: ${ll.HighlightText};
          border-color: ${ll.Highlight};
          color: ${ll.Highlight};
        }

        :host(${r}) .control {
          background: transparent;
          border-color: ${ll.GrayText};
          color: ${ll.GrayText};
        }

        .control:${ol} {
          outline-color: ${ll.CanvasText};
          box-shadow: 0 0 0 calc(${gr} * 1px) ${ll.HighlightText} inset !important;
        }

        :host([href]) .control {
          background: ${ll.LinkText};
          color: ${ll.HighlightText};
        }

        :host([href]:hover) .control,
        :host([href]:active) .control {
          background: ${ll.ButtonFace};
          border-color: ${ll.LinkText};
          color: ${ll.LinkText};
        }
      `)),Cl=(e,t,n,r="[disabled]")=>Yt`
    :host {
      height: auto;
      font-family: inherit;
      font-size: inherit;
      line-height: inherit;
      min-width: 0;
    }

    .control {
      display: inline;
      padding: 0;
      border: none;
      box-shadow: none;
      line-height: 1;
    }

    :host(${n}) .control {
      color: ${$i};
      text-decoration: underline 1px;
    }

    :host(${n}:hover) .control {
      color: ${wi};
      text-decoration: none;
    }

    :host(${n}:active) .control {
      color: ${xi};
      text-decoration: none;
    }

    .control:${ol} {
      ${dl}
    }
  `.withBehaviors(sl(Yt`
        :host(${n}) .control {
          color: ${ll.LinkText};
        }

        :host(${n}:hover) .control,
        :host(${n}:active) .control {
          color: ${ll.CanvasText};
        }

        .control:${ol} {
          outline-color: ${ll.CanvasText};
        }
      `)),Ll=(e,t,n,r="[disabled]")=>Yt`
    :host {
      color: ${$i};
    }

    .control {
      background: ${ra};
    }

    :host(${n}:hover) .control {
      background: ${oa};
      color: ${wi};
    }

    :host(${n}:active) .control {
      background: ${ia};
      color: ${xi};
    }

    :host(${r}) .control {
      background: ${ra};
    }
  `.withBehaviors(sl(Yt`
        :host {
          color: ${ll.ButtonText};
        }

        .control {
          forced-color-adjust: none;
          background: transparent;
        }

        :host(${n}:hover) .control,
        :host(${n}:active) .control {
          background: transparent;
          border-color: ${ll.ButtonText};
          color: ${ll.ButtonText};
        }

        :host(${r}) .control {
          background: transparent;
          color: ${ll.GrayText};
        }

        .control:${ol} {
          outline-color: ${ll.CanvasText};
        }

        :host([href]) .control {
          color: ${ll.LinkText};
        }

        :host([href]:hover) .control,
        :host([href]:active) .control {
          border-color: ${ll.LinkText};
          color: ${ll.LinkText};
        }
      `)),Dl=(e,t,n,r="[disabled]")=>Yt`
    .control {
      background: transparent !important;
      border-color: ${_a};
    }

    :host(${n}:hover) .control {
      border-color: ${$a};
    }

    :host(${n}:active) .control {
      border-color: ${wa};
    }

    :host(${r}) .control {
      background: transparent !important;
      border-color: ${_a};
    }
  `.withBehaviors(sl(Yt`
        .control {
          border-color: ${ll.ButtonText};
          color: ${ll.ButtonText};
        }

        :host(${n}:hover) .control,
        :host(${n}:active) .control {
          background: ${ll.HighlightText};
          border-color: ${ll.Highlight};
          color: ${ll.Highlight};
        }

        :host(${r}) .control {
          border-color: ${ll.GrayText};
          color: ${ll.GrayText};
        }

        .control:${ol} {
          outline-color: ${ll.CanvasText};
        }

        :host([href]) .control {
          border-color: ${ll.LinkText};
          color: ${ll.LinkText};
        }

        :host([href]:hover) .control,
        :host([href]:active) .control {
          border-color: ${ll.CanvasText};
          color: ${ll.CanvasText};
        }
      `)),El=(e,t,n,r="[disabled]")=>Yt`
    .control {
      background: ${ra};
    }

    :host(${n}:hover) .control {
      background: ${oa};
    }

    :host(${n}:active) .control {
      background: ${ia};
    }

    :host(${r}) .control {
      background: ${ra};
    }
  `.withBehaviors(sl(Yt`
        .control {
          forced-color-adjust: none;
          background: transparent;
          color: ${ll.ButtonText};
        }

        :host(${n}:hover) .control,
        :host(${n}:active) .control {
          background: transparent;
          border-color: ${ll.ButtonText};
          color: ${ll.ButtonText};
        }

        :host(${r}) .control {
          background: transparent;
          color: ${ll.GrayText};
        }
        
        .control:${ol} {
          outline-color: ${ll.CanvasText};
        }

        :host([href]) .control {
          color: ${ll.LinkText};
        }

        :host([href]:hover) .control,
        :host([href]:active) .control {
          background: transparent;
          border-color: ${ll.LinkText};
          color: ${ll.LinkText};
        }
      `));class Al{constructor(e,t,n){this.propertyName=e,this.value=t,this.styles=n}bind(e){v.getNotifier(e).subscribe(this,this.propertyName),this.handleChange(e,this.propertyName)}unbind(e){v.getNotifier(e).unsubscribe(this,this.propertyName),e.$fastController.removeStyles(this.styles)}handleChange(e,t){e[t]===this.value?e.$fastController.addStyles(this.styles):e.$fastController.removeStyles(this.styles)}}function Nl(e,t){return new Al("appearance",e,t)}const Ol="[href]",Pl=(e,t)=>kl(e,t,Ol).withBehaviors(Nl("neutral",Sl(e,t,Ol)),Nl("accent",Ml(e,t,Ol)),Nl("hypertext",Cl(e,t,Ol)),Nl("lightweight",Ll(e,t,Ol)),Nl("outline",Dl(e,t,Ol)),Nl("stealth",El(e,t,Ol)));class Il extends wl{appearanceChanged(e,t){e!==t&&(this.classList.add(t),this.classList.remove(e))}connectedCallback(){super.connectedCallback(),this.appearance||(this.appearance="neutral")}defaultSlottedContentChanged(){const e=this.defaultSlottedContent.filter((e=>e.nodeType===Node.ELEMENT_NODE));1===e.length&&e[0]instanceof SVGElement?this.control.classList.add("icon-only"):this.control.classList.remove("icon-only")}}_l([M],Il.prototype,"appearance",void 0);const Rl=Pl,Fl=Il.compose({baseName:"anchor",baseClass:wl,template:Tl,styles:Pl,shadowOptions:{delegatesFocus:!0}}),Yl="focus",jl="focusin",Hl="focusout",Ul="keydown",Bl="resize",Vl="scroll",zl=e=>{const t=e.closest("[dir]");return null!==t&&"rtl"===t.dir?un.rtl:un.ltr};class Wl extends ze{constructor(){super(...arguments),this.anchor="",this.viewport="",this.horizontalPositioningMode="uncontrolled",this.horizontalDefaultPosition="unset",this.horizontalViewportLock=!1,this.horizontalInset=!1,this.horizontalScaling="content",this.verticalPositioningMode="uncontrolled",this.verticalDefaultPosition="unset",this.verticalViewportLock=!1,this.verticalInset=!1,this.verticalScaling="content",this.fixedPlacement=!1,this.autoUpdateMode="anchor",this.anchorElement=null,this.viewportElement=null,this.initialLayoutComplete=!1,this.resizeDetector=null,this.baseHorizontalOffset=0,this.baseVerticalOffset=0,this.pendingPositioningUpdate=!1,this.pendingReset=!1,this.currentDirection=un.ltr,this.regionVisible=!1,this.forceUpdate=!1,this.updateThreshold=.5,this.update=()=>{this.pendingPositioningUpdate||this.requestPositionUpdates()},this.startObservers=()=>{this.stopObservers(),null!==this.anchorElement&&(this.requestPositionUpdates(),null!==this.resizeDetector&&(this.resizeDetector.observe(this.anchorElement),this.resizeDetector.observe(this)))},this.requestPositionUpdates=()=>{null===this.anchorElement||this.pendingPositioningUpdate||(Wl.intersectionService.requestPosition(this,this.handleIntersection),Wl.intersectionService.requestPosition(this.anchorElement,this.handleIntersection),null!==this.viewportElement&&Wl.intersectionService.requestPosition(this.viewportElement,this.handleIntersection),this.pendingPositioningUpdate=!0)},this.stopObservers=()=>{this.pendingPositioningUpdate&&(this.pendingPositioningUpdate=!1,Wl.intersectionService.cancelRequestPosition(this,this.handleIntersection),null!==this.anchorElement&&Wl.intersectionService.cancelRequestPosition(this.anchorElement,this.handleIntersection),null!==this.viewportElement&&Wl.intersectionService.cancelRequestPosition(this.viewportElement,this.handleIntersection)),null!==this.resizeDetector&&this.resizeDetector.disconnect()},this.getViewport=()=>"string"!=typeof this.viewport||""===this.viewport?document.documentElement:document.getElementById(this.viewport),this.getAnchor=()=>document.getElementById(this.anchor),this.handleIntersection=e=>{this.pendingPositioningUpdate&&(this.pendingPositioningUpdate=!1,this.applyIntersectionEntries(e)&&this.updateLayout())},this.applyIntersectionEntries=e=>{const t=e.find((e=>e.target===this)),n=e.find((e=>e.target===this.anchorElement)),r=e.find((e=>e.target===this.viewportElement));return void 0!==t&&void 0!==r&&void 0!==n&&(!!(!this.regionVisible||this.forceUpdate||void 0===this.regionRect||void 0===this.anchorRect||void 0===this.viewportRect||this.isRectDifferent(this.anchorRect,n.boundingClientRect)||this.isRectDifferent(this.viewportRect,r.boundingClientRect)||this.isRectDifferent(this.regionRect,t.boundingClientRect))&&(this.regionRect=t.boundingClientRect,this.anchorRect=n.boundingClientRect,this.viewportElement===document.documentElement?this.viewportRect=new DOMRectReadOnly(r.boundingClientRect.x+document.documentElement.scrollLeft,r.boundingClientRect.y+document.documentElement.scrollTop,r.boundingClientRect.width,r.boundingClientRect.height):this.viewportRect=r.boundingClientRect,this.updateRegionOffset(),this.forceUpdate=!1,!0))},this.updateRegionOffset=()=>{this.anchorRect&&this.regionRect&&(this.baseHorizontalOffset=this.baseHorizontalOffset+(this.anchorRect.left-this.regionRect.left)+(this.translateX-this.baseHorizontalOffset),this.baseVerticalOffset=this.baseVerticalOffset+(this.anchorRect.top-this.regionRect.top)+(this.translateY-this.baseVerticalOffset))},this.isRectDifferent=(e,t)=>Math.abs(e.top-t.top)>this.updateThreshold||Math.abs(e.right-t.right)>this.updateThreshold||Math.abs(e.bottom-t.bottom)>this.updateThreshold||Math.abs(e.left-t.left)>this.updateThreshold,this.handleResize=e=>{this.update()},this.reset=()=>{this.pendingReset&&(this.pendingReset=!1,null===this.anchorElement&&(this.anchorElement=this.getAnchor()),null===this.viewportElement&&(this.viewportElement=this.getViewport()),this.currentDirection=zl(this),this.startObservers())},this.updateLayout=()=>{let e,t;if("uncontrolled"!==this.horizontalPositioningMode){const e=this.getPositioningOptions(this.horizontalInset);if("center"===this.horizontalDefaultPosition)t="center";else if("unset"!==this.horizontalDefaultPosition){let e=this.horizontalDefaultPosition;if("start"===e||"end"===e){const t=zl(this);if(t!==this.currentDirection)return this.currentDirection=t,void this.initialize();e=this.currentDirection===un.ltr?"start"===e?"left":"right":"start"===e?"right":"left"}switch(e){case"left":t=this.horizontalInset?"insetStart":"start";break;case"right":t=this.horizontalInset?"insetEnd":"end"}}const n=void 0!==this.horizontalThreshold?this.horizontalThreshold:void 0!==this.regionRect?this.regionRect.width:0,r=void 0!==this.anchorRect?this.anchorRect.left:0,o=void 0!==this.anchorRect?this.anchorRect.right:0,i=void 0!==this.anchorRect?this.anchorRect.width:0,a=void 0!==this.viewportRect?this.viewportRect.left:0,s=void 0!==this.viewportRect?this.viewportRect.right:0;(void 0===t||"locktodefault"!==this.horizontalPositioningMode&&this.getAvailableSpace(t,r,o,i,a,s)<n)&&(t=this.getAvailableSpace(e[0],r,o,i,a,s)>this.getAvailableSpace(e[1],r,o,i,a,s)?e[0]:e[1])}if("uncontrolled"!==this.verticalPositioningMode){const t=this.getPositioningOptions(this.verticalInset);if("center"===this.verticalDefaultPosition)e="center";else if("unset"!==this.verticalDefaultPosition)switch(this.verticalDefaultPosition){case"top":e=this.verticalInset?"insetStart":"start";break;case"bottom":e=this.verticalInset?"insetEnd":"end"}const n=void 0!==this.verticalThreshold?this.verticalThreshold:void 0!==this.regionRect?this.regionRect.height:0,r=void 0!==this.anchorRect?this.anchorRect.top:0,o=void 0!==this.anchorRect?this.anchorRect.bottom:0,i=void 0!==this.anchorRect?this.anchorRect.height:0,a=void 0!==this.viewportRect?this.viewportRect.top:0,s=void 0!==this.viewportRect?this.viewportRect.bottom:0;(void 0===e||"locktodefault"!==this.verticalPositioningMode&&this.getAvailableSpace(e,r,o,i,a,s)<n)&&(e=this.getAvailableSpace(t[0],r,o,i,a,s)>this.getAvailableSpace(t[1],r,o,i,a,s)?t[0]:t[1])}const n=this.getNextRegionDimension(t,e),r=this.horizontalPosition!==t||this.verticalPosition!==e;if(this.setHorizontalPosition(t,n),this.setVerticalPosition(e,n),this.updateRegionStyle(),!this.initialLayoutComplete)return this.initialLayoutComplete=!0,void this.requestPositionUpdates();this.regionVisible||(this.regionVisible=!0,this.style.removeProperty("pointer-events"),this.style.removeProperty("opacity"),this.classList.toggle("loaded",!0),this.$emit("loaded",this,{bubbles:!1})),this.updatePositionClasses(),r&&this.$emit("positionchange",this,{bubbles:!1})},this.updateRegionStyle=()=>{this.style.width=this.regionWidth,this.style.height=this.regionHeight,this.style.transform=`translate(${this.translateX}px, ${this.translateY}px)`},this.updatePositionClasses=()=>{this.classList.toggle("top","start"===this.verticalPosition),this.classList.toggle("bottom","end"===this.verticalPosition),this.classList.toggle("inset-top","insetStart"===this.verticalPosition),this.classList.toggle("inset-bottom","insetEnd"===this.verticalPosition),this.classList.toggle("vertical-center","center"===this.verticalPosition),this.classList.toggle("left","start"===this.horizontalPosition),this.classList.toggle("right","end"===this.horizontalPosition),this.classList.toggle("inset-left","insetStart"===this.horizontalPosition),this.classList.toggle("inset-right","insetEnd"===this.horizontalPosition),this.classList.toggle("horizontal-center","center"===this.horizontalPosition)},this.setHorizontalPosition=(e,t)=>{if(void 0===e||void 0===this.regionRect||void 0===this.anchorRect||void 0===this.viewportRect)return;let n=0;switch(this.horizontalScaling){case"anchor":case"fill":n=this.horizontalViewportLock?this.viewportRect.width:t.width,this.regionWidth=`${n}px`;break;case"content":n=this.regionRect.width,this.regionWidth="unset"}let r=0;switch(e){case"start":this.translateX=this.baseHorizontalOffset-n,this.horizontalViewportLock&&this.anchorRect.left>this.viewportRect.right&&(this.translateX=this.translateX-(this.anchorRect.left-this.viewportRect.right));break;case"insetStart":this.translateX=this.baseHorizontalOffset-n+this.anchorRect.width,this.horizontalViewportLock&&this.anchorRect.right>this.viewportRect.right&&(this.translateX=this.translateX-(this.anchorRect.right-this.viewportRect.right));break;case"insetEnd":this.translateX=this.baseHorizontalOffset,this.horizontalViewportLock&&this.anchorRect.left<this.viewportRect.left&&(this.translateX=this.translateX-(this.anchorRect.left-this.viewportRect.left));break;case"end":this.translateX=this.baseHorizontalOffset+this.anchorRect.width,this.horizontalViewportLock&&this.anchorRect.right<this.viewportRect.left&&(this.translateX=this.translateX-(this.anchorRect.right-this.viewportRect.left));break;case"center":if(r=(this.anchorRect.width-n)/2,this.translateX=this.baseHorizontalOffset+r,this.horizontalViewportLock){const e=this.anchorRect.left+r,t=this.anchorRect.right-r;e<this.viewportRect.left&&!(t>this.viewportRect.right)?this.translateX=this.translateX-(e-this.viewportRect.left):t>this.viewportRect.right&&!(e<this.viewportRect.left)&&(this.translateX=this.translateX-(t-this.viewportRect.right))}}this.horizontalPosition=e},this.setVerticalPosition=(e,t)=>{if(void 0===e||void 0===this.regionRect||void 0===this.anchorRect||void 0===this.viewportRect)return;let n=0;switch(this.verticalScaling){case"anchor":case"fill":n=this.verticalViewportLock?this.viewportRect.height:t.height,this.regionHeight=`${n}px`;break;case"content":n=this.regionRect.height,this.regionHeight="unset"}let r=0;switch(e){case"start":this.translateY=this.baseVerticalOffset-n,this.verticalViewportLock&&this.anchorRect.top>this.viewportRect.bottom&&(this.translateY=this.translateY-(this.anchorRect.top-this.viewportRect.bottom));break;case"insetStart":this.translateY=this.baseVerticalOffset-n+this.anchorRect.height,this.verticalViewportLock&&this.anchorRect.bottom>this.viewportRect.bottom&&(this.translateY=this.translateY-(this.anchorRect.bottom-this.viewportRect.bottom));break;case"insetEnd":this.translateY=this.baseVerticalOffset,this.verticalViewportLock&&this.anchorRect.top<this.viewportRect.top&&(this.translateY=this.translateY-(this.anchorRect.top-this.viewportRect.top));break;case"end":this.translateY=this.baseVerticalOffset+this.anchorRect.height,this.verticalViewportLock&&this.anchorRect.bottom<this.viewportRect.top&&(this.translateY=this.translateY-(this.anchorRect.bottom-this.viewportRect.top));break;case"center":if(r=(this.anchorRect.height-n)/2,this.translateY=this.baseVerticalOffset+r,this.verticalViewportLock){const e=this.anchorRect.top+r,t=this.anchorRect.bottom-r;e<this.viewportRect.top&&!(t>this.viewportRect.bottom)?this.translateY=this.translateY-(e-this.viewportRect.top):t>this.viewportRect.bottom&&!(e<this.viewportRect.top)&&(this.translateY=this.translateY-(t-this.viewportRect.bottom))}}this.verticalPosition=e},this.getPositioningOptions=e=>e?["insetStart","insetEnd"]:["start","end"],this.getAvailableSpace=(e,t,n,r,o,i)=>{const a=t-o,s=i-(t+r);switch(e){case"start":return a;case"insetStart":return a+r;case"insetEnd":return s+r;case"end":return s;case"center":return 2*Math.min(a,s)+r}},this.getNextRegionDimension=(e,t)=>{const n={height:void 0!==this.regionRect?this.regionRect.height:0,width:void 0!==this.regionRect?this.regionRect.width:0};return void 0!==e&&"fill"===this.horizontalScaling?n.width=this.getAvailableSpace(e,void 0!==this.anchorRect?this.anchorRect.left:0,void 0!==this.anchorRect?this.anchorRect.right:0,void 0!==this.anchorRect?this.anchorRect.width:0,void 0!==this.viewportRect?this.viewportRect.left:0,void 0!==this.viewportRect?this.viewportRect.right:0):"anchor"===this.horizontalScaling&&(n.width=void 0!==this.anchorRect?this.anchorRect.width:0),void 0!==t&&"fill"===this.verticalScaling?n.height=this.getAvailableSpace(t,void 0!==this.anchorRect?this.anchorRect.top:0,void 0!==this.anchorRect?this.anchorRect.bottom:0,void 0!==this.anchorRect?this.anchorRect.height:0,void 0!==this.viewportRect?this.viewportRect.top:0,void 0!==this.viewportRect?this.viewportRect.bottom:0):"anchor"===this.verticalScaling&&(n.height=void 0!==this.anchorRect?this.anchorRect.height:0),n},this.startAutoUpdateEventListeners=()=>{window.addEventListener(Bl,this.update,{passive:!0}),window.addEventListener(Vl,this.update,{passive:!0,capture:!0}),null!==this.resizeDetector&&null!==this.viewportElement&&this.resizeDetector.observe(this.viewportElement)},this.stopAutoUpdateEventListeners=()=>{window.removeEventListener(Bl,this.update),window.removeEventListener(Vl,this.update),null!==this.resizeDetector&&null!==this.viewportElement&&this.resizeDetector.unobserve(this.viewportElement)}}anchorChanged(){this.initialLayoutComplete&&(this.anchorElement=this.getAnchor())}viewportChanged(){this.initialLayoutComplete&&(this.viewportElement=this.getViewport())}horizontalPositioningModeChanged(){this.requestReset()}horizontalDefaultPositionChanged(){this.updateForAttributeChange()}horizontalViewportLockChanged(){this.updateForAttributeChange()}horizontalInsetChanged(){this.updateForAttributeChange()}horizontalThresholdChanged(){this.updateForAttributeChange()}horizontalScalingChanged(){this.updateForAttributeChange()}verticalPositioningModeChanged(){this.requestReset()}verticalDefaultPositionChanged(){this.updateForAttributeChange()}verticalViewportLockChanged(){this.updateForAttributeChange()}verticalInsetChanged(){this.updateForAttributeChange()}verticalThresholdChanged(){this.updateForAttributeChange()}verticalScalingChanged(){this.updateForAttributeChange()}fixedPlacementChanged(){this.$fastController.isConnected&&this.initialLayoutComplete&&this.initialize()}autoUpdateModeChanged(e,t){this.$fastController.isConnected&&this.initialLayoutComplete&&("auto"===e&&this.stopAutoUpdateEventListeners(),"auto"===t&&this.startAutoUpdateEventListeners())}anchorElementChanged(){this.requestReset()}viewportElementChanged(){this.$fastController.isConnected&&this.initialLayoutComplete&&this.initialize()}connectedCallback(){super.connectedCallback(),"auto"===this.autoUpdateMode&&this.startAutoUpdateEventListeners(),this.initialize()}disconnectedCallback(){super.disconnectedCallback(),"auto"===this.autoUpdateMode&&this.stopAutoUpdateEventListeners(),this.stopObservers(),this.disconnectResizeDetector()}adoptedCallback(){this.initialize()}disconnectResizeDetector(){null!==this.resizeDetector&&(this.resizeDetector.disconnect(),this.resizeDetector=null)}initializeResizeDetector(){this.disconnectResizeDetector(),this.resizeDetector=new window.ResizeObserver(this.handleResize)}updateForAttributeChange(){this.$fastController.isConnected&&this.initialLayoutComplete&&(this.forceUpdate=!0,this.update())}initialize(){this.initializeResizeDetector(),null===this.anchorElement&&(this.anchorElement=this.getAnchor()),this.requestReset()}requestReset(){this.$fastController.isConnected&&!1===this.pendingReset&&(this.setInitialState(),m.queueUpdate((()=>this.reset())),this.pendingReset=!0)}setInitialState(){this.initialLayoutComplete=!1,this.regionVisible=!1,this.translateX=0,this.translateY=0,this.baseHorizontalOffset=0,this.baseVerticalOffset=0,this.viewportRect=void 0,this.regionRect=void 0,this.anchorRect=void 0,this.verticalPosition=void 0,this.horizontalPosition=void 0,this.style.opacity="0",this.style.pointerEvents="none",this.forceUpdate=!1,this.style.position=this.fixedPlacement?"fixed":"absolute",this.updatePositionClasses(),this.updateRegionStyle()}}function Gl(e,t){const n="function"==typeof t?t:()=>t;return(t,r)=>e(t,r)?n(t,r):null}Wl.intersectionService=new class{constructor(){this.intersectionDetector=null,this.observedElements=new Map,this.requestPosition=(e,t)=>{var n;null!==this.intersectionDetector&&(this.observedElements.has(e)?null===(n=this.observedElements.get(e))||void 0===n||n.push(t):(this.observedElements.set(e,[t]),this.intersectionDetector.observe(e)))},this.cancelRequestPosition=(e,t)=>{const n=this.observedElements.get(e);if(void 0!==n){const e=n.indexOf(t);-1!==e&&n.splice(e,1)}},this.initializeIntersectionDetector=()=>{o.IntersectionObserver&&(this.intersectionDetector=new IntersectionObserver(this.handleIntersection,{root:null,rootMargin:"0px",threshold:[0,1]}))},this.handleIntersection=e=>{if(null===this.intersectionDetector)return;const t=[],n=[];e.forEach((e=>{var r;null===(r=this.intersectionDetector)||void 0===r||r.unobserve(e.target);const o=this.observedElements.get(e.target);void 0!==o&&(o.forEach((r=>{let o=t.indexOf(r);-1===o&&(o=t.length,t.push(r),n.push([])),n[o].push(e)})),this.observedElements.delete(e.target))})),t.forEach(((e,t)=>{e(n[t])}))},this.initializeIntersectionDetector()}},r([M],Wl.prototype,"anchor",void 0),r([M],Wl.prototype,"viewport",void 0),r([M({attribute:"horizontal-positioning-mode"})],Wl.prototype,"horizontalPositioningMode",void 0),r([M({attribute:"horizontal-default-position"})],Wl.prototype,"horizontalDefaultPosition",void 0),r([M({attribute:"horizontal-viewport-lock",mode:"boolean"})],Wl.prototype,"horizontalViewportLock",void 0),r([M({attribute:"horizontal-inset",mode:"boolean"})],Wl.prototype,"horizontalInset",void 0),r([M({attribute:"horizontal-threshold"})],Wl.prototype,"horizontalThreshold",void 0),r([M({attribute:"horizontal-scaling"})],Wl.prototype,"horizontalScaling",void 0),r([M({attribute:"vertical-positioning-mode"})],Wl.prototype,"verticalPositioningMode",void 0),r([M({attribute:"vertical-default-position"})],Wl.prototype,"verticalDefaultPosition",void 0),r([M({attribute:"vertical-viewport-lock",mode:"boolean"})],Wl.prototype,"verticalViewportLock",void 0),r([M({attribute:"vertical-inset",mode:"boolean"})],Wl.prototype,"verticalInset",void 0),r([M({attribute:"vertical-threshold"})],Wl.prototype,"verticalThreshold",void 0),r([M({attribute:"vertical-scaling"})],Wl.prototype,"verticalScaling",void 0),r([M({attribute:"fixed-placement",mode:"boolean"})],Wl.prototype,"fixedPlacement",void 0),r([M({attribute:"auto-update-mode"})],Wl.prototype,"autoUpdateMode",void 0),r([b],Wl.prototype,"anchorElement",void 0),r([b],Wl.prototype,"viewportElement",void 0),r([b],Wl.prototype,"initialLayoutComplete",void 0);const ql=(e,t)=>Yt`
  :host {
  }

