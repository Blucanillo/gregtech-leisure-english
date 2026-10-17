ForgeEvents.onEvent("net.minecraftforge.event.entity.player.ItemTooltipEvent", event => {
    if (!LDLib.isClient()) return
    // Native GTMThings duration text is a literal child component. Keep the
    // energy component, original duration, and styles; translate that child only.
    var digitalMinerIds = ["gtmthings:lv_digital_miner", "gtmthings:mv_digital_miner", "gtmthings:hv_digital_miner"]
    var tooltipItemId = String(event.getItemStack().getId())
    if (digitalMinerIds.indexOf(tooltipItemId) >= 0) {
        var digitalMinerLines = event.getToolTip()
        for (var minerLineIndex = 0; minerLineIndex < digitalMinerLines.size(); minerLineIndex++) {
            var minerSiblings = digitalMinerLines.get(minerLineIndex).getSiblings()
            for (var minerChildIndex = 0; minerChildIndex < minerSiblings.size(); minerChildIndex++) {
                var minerChild = minerSiblings.get(minerChildIndex)
                var minerDuration = /^§7\u6bcf\u4e2a\u65b9\u5757\u9700\u8981§f(\d+)§7\u523b。$/.exec(String(minerChild.getString()))
                if (minerDuration) {
                    minerSiblings.set(minerChildIndex, Component.translatable("gtl1450.tooltip.digital_miner_ticks", minerDuration[1]).setStyle(minerChild.getStyle()))
                }
            }
        }
    }
    // Some Core material/generator hints are native literal components too.
    // Match the exact original text; changed wording/numbers in another version
    // will not be overwritten by a stale translation.
    if (tooltipItemId.indexOf("gtceu:") === 0 && (tooltipItemId.indexOf("spacetime") >= 0 || tooltipItemId === "gtceu:chemical_energy_devourer")) {
        var literalTranslations = {"\u00a77\u7194\u70bc\u4e3a\u6d41\u4f53\u7684\u65f6\u7a7a": "gtl1450.tooltip.spacetime_fluid_hint", "\u63d0\u4f9b\u00a7f120mB/s\u00a77\u7684\u6db2\u6001\u6c27\uff0c\u5e76\u6d88\u8017\u00a7f\u53cc\u500d\u00a77\u71c3\u6599\u4ee5\u4ea7\u751f\u9ad8\u8fbe\u00a7f1048576\u00a77EU/t\u7684\u529f\u7387\u3002": "gtl1450.tooltip.chemical_devourer_oxygen", "\u518d\u989d\u5916\u63d0\u4f9b\u00a7f80mB/s\u00a77\u7684\u56db\u6c27\u5316\u4e8c\u6c2e\uff0c\u5e76\u6d88\u8017\u00a7f\u56db\u500d\u00a77\u71c3\u6599\u4ee5\u4ea7\u751f\u9ad8\u8fbe\u00a7f4194304\u00a77EU/t\u7684\u529f\u7387\u3002": "gtl1450.tooltip.chemical_devourer_tetroxide"}
        var coreTooltipLines = event.getToolTip()
        for (var coreLineIndex = 0; coreLineIndex < coreTooltipLines.size(); coreLineIndex++) {
            var coreLine = coreTooltipLines.get(coreLineIndex)
            var originalLiteral = String(coreLine.getString())
            if (Object.prototype.hasOwnProperty.call(literalTranslations, originalLiteral)) {
                coreTooltipLines.set(coreLineIndex, Component.translatable(literalTranslations[originalLiteral]).setStyle(coreLine.getStyle()))
            }
        }
    }
    function display_tier(tier) {
        if (tier === "luv") return "LuV"
        if (tier === "opv") return "OpV"
        return tier.toUpperCase()
    }
    // Resolve the translation key to its English string on the client, then let the
    // GTLcore TextUtil helpers build the same colour / gradient ramp they always did.
    function text(key, args) {
        return args === undefined ? Component.translatable(key).string : Component.translatable(key, args).string
    }
    // TextUtil walks its colour cycle once per character of whatever it is handed, so
    // gradient inputs must be plain visible text.  If a value ever carries a § code it
    // is stripped here rather than being painted as literal characters.
    // Component.translatable(key).string hands back a *wrapped Java String*, not a
    // JavaScript string: typeof is "object", and reading .length finds Java's length()
    // method rather than a number.  A loop written as "while (i < text.length)" therefore
    // never executes and silently returns "", which renders as an empty tooltip line.
    // Coerce to a real JavaScript string first, then drop the colour codes with a regex.
    function clean(value) {
        return ("" + value).replace(/\u00a7./g, "").replace(/\u00a7/g, "")
    }
    // The ramp must cover the whole phrase, not just the tier code.  TextUtil walks its
    // colour cycle per character, and a 2-character code such as "LV" lands on the same
    // colour twice, which renders as flat.  "LV Circuit" is long enough for the cycle to
    // show, and this matches the original, where the ramp covered a 6-character phrase.
    function tier_line(tier) {
        return TextUtil.white_blue(clean(text("gtl1450.tooltip.circuit_tier_plain", tier)))
    }
    function tier_ramp(key, fn) {
        return fn(clean(text(key)))
    }
    function addfull_colortooltip(key) {
        event.getToolTip().add(Component.literal(ramp(TextUtil.full_color, key)))
    }
    function adddark_purplish_redtooltip(key) {
        event.getToolTip().add(Component.literal(ramp(TextUtil.dark_purplish_red, key)))
    }
    function addwhite_bluetooltip(key, arg) {
        event.getToolTip().add(Component.literal(ramp(TextUtil.white_blue, key, arg)))
    }
    function addpurplish_redtooltip(key) {
        event.getToolTip().add(Component.literal(ramp(TextUtil.purplish_red, key)))
    }
    function addgoldentooltip(key) {
        event.getToolTip().add(Component.literal(ramp(TextUtil.golden, key)))
    }
    function adddark_greentooltip(key) {
        event.getToolTip().add(Component.literal(ramp(TextUtil.dark_green, key)))
    }
    function ramp(fn, key, args) {
        return fn(clean(text(key, args)))
    }
    function addfull_colortier(key) {
        event.getToolTip().add(Component.literal(tier_ramp(key, TextUtil.full_color)))
    }
    function adddark_purplish_redtier(key) {
        event.getToolTip().add(Component.literal(tier_ramp(key, TextUtil.dark_purplish_red)))
    }
    function addpurplish_redtier(key) {
        event.getToolTip().add(Component.literal(tier_ramp(key, TextUtil.purplish_red)))
    }
    function addgoldentier(key) {
        event.getToolTip().add(Component.literal(tier_ramp(key, TextUtil.golden)))
    }
    function adddark_greentier(key) {
        event.getToolTip().add(Component.literal(tier_ramp(key, TextUtil.dark_green)))
    }
    function addtooltip(key) {
        event.getToolTip().add(Component.literal("\u00a77" + text(key)))
    }
    function unknown() {
        addtooltip("gtl1450.tooltip.device_unusable")
        event.getToolTip().add(Component.literal("\u00a72" + text("gtl1450.tooltip.tier_prefix")).append(Component.literal(ramp(TextUtil.white_blue, "gtl1450.tooltip.unknown"))))
    }
    const tiers = ["ulv", "lv", "mv", "hv", "ev", "iv", "luv", "zpm", "uv", "uhv", "uev", "uiv", "uxv", "opv", "max"]
    tiers.forEach((suprachronal) => {
        if (event.getItemStack().getId() == "kubejs:suprachronal_" + suprachronal) {
            addtooltip("gtl1450.tooltip.suprachronal")
            event.getToolTip().add(Component.literal("\u00a77" + tier_line(display_tier(suprachronal))))
        }
    })
    tiers.slice(0, 12).forEach((magneto_resonatic) => {
        if (event.getItemStack().getId() == "kubejs:circuit_resonatic_" + magneto_resonatic) {
            event.getToolTip().add(Component.literal("\u00a77\u00a7d" + display_tier(magneto_resonatic) + text("gtl1450.tooltip.circuit_suffix")))
        }
    })
    switch (event.getItemStack().getId()) {
        case "gtceu:dimensionally_transcendent_dirt_forge":
            addfull_colortooltip("gtl1450.tooltip.dirt_forge")
            break
        case "gtceu:door_of_create":
            addwhite_bluetooltip("gtl1450.tooltip.door_of_create")
            break
        case "kubejs:create_ultimate_battery":
            addtooltip("gtl1450.tooltip.create_ultimate_battery")
            unknown()
            break
        case "kubejs:suprachronal_mainframe_complex":
            addtooltip("gtl1450.tooltip.suprachronal_mainframe_complex")
            unknown()
            break
        case "kubejs:supracausal_mainframe":
            addtooltip("gtl1450.tooltip.supracausal_mainframe")
            addfull_colortier("gtl1450.tooltip.circuit_max_plain")
            break
        case "kubejs:supracausal_computer":
            addtooltip("gtl1450.tooltip.supracausal_computer")
            addfull_colortier("gtl1450.tooltip.circuit_opv_plain")
            break
        case "kubejs:supracausal_assembly":
            addtooltip("gtl1450.tooltip.supracausal_assembly")
            addfull_colortier("gtl1450.tooltip.circuit_uxv_plain")
            break
        case "kubejs:supracausal_processor":
            addtooltip("gtl1450.tooltip.supracausal_processor")
            addfull_colortier("gtl1450.tooltip.circuit_uiv_plain")
            break
        case "kubejs:cosmic_assembly":
            addtooltip("gtl1450.tooltip.cosmic_assembly")
            adddark_purplish_redtier("gtl1450.tooltip.circuit_uiv_plain")
            break
        case "kubejs:cosmic_computer":
            addtooltip("gtl1450.tooltip.cosmic_computer")
            adddark_purplish_redtier("gtl1450.tooltip.circuit_uxv_plain")
            break
        case "kubejs:cosmic_mainframe":
            addtooltip("gtl1450.tooltip.cosmic_mainframe")
            adddark_purplish_redtier("gtl1450.tooltip.circuit_opv_plain")
            break
        case "kubejs:cosmic_processor":
            addtooltip("gtl1450.tooltip.cosmic_processor")
            adddark_purplish_redtier("gtl1450.tooltip.circuit_uev_plain")
            break
        case "kubejs:exotic_assembly":
            addtooltip("gtl1450.tooltip.exotic_assembly")
            addpurplish_redtier("gtl1450.tooltip.circuit_uev_plain")
            break
        case "kubejs:exotic_computer":
            addtooltip("gtl1450.tooltip.exotic_computer")
            addpurplish_redtier("gtl1450.tooltip.circuit_uiv_plain")
            break
        case "kubejs:exotic_mainframe":
            addtooltip("gtl1450.tooltip.exotic_mainframe")
            addpurplish_redtier("gtl1450.tooltip.circuit_uxv_plain")
            break
        case "kubejs:exotic_processor":
            addtooltip("gtl1450.tooltip.exotic_processor")
            addpurplish_redtier("gtl1450.tooltip.circuit_uhv_plain")
            break
        case "kubejs:optical_assembly":
            addtooltip("gtl1450.tooltip.optical_assembly")
            addgoldentier("gtl1450.tooltip.circuit_uhv_plain")
            break
        case "kubejs:optical_computer":
            addtooltip("gtl1450.tooltip.optical_computer")
            addgoldentier("gtl1450.tooltip.circuit_uev_plain")
            break
        case "kubejs:optical_mainframe":
            addtooltip("gtl1450.tooltip.optical_mainframe")
            addgoldentier("gtl1450.tooltip.circuit_uiv_plain")
            break
        case "kubejs:optical_processor":
            addtooltip("gtl1450.tooltip.optical_processor")
            addgoldentier("gtl1450.tooltip.circuit_uv_plain")
            break
        case "kubejs:bioware_assembly":
            addtooltip("gtl1450.tooltip.bioware_assembly")
            adddark_greentier("gtl1450.tooltip.circuit_uv_plain")
            break
        case "kubejs:bioware_computer":
            addtooltip("gtl1450.tooltip.bioware_computer")
            adddark_greentier("gtl1450.tooltip.circuit_uhv_plain")
            break
        case "kubejs:bioware_mainframe":
            addtooltip("gtl1450.tooltip.bioware_mainframe")
            adddark_greentier("gtl1450.tooltip.circuit_uev_plain")
            break
        case "kubejs:bioware_processor":
            addtooltip("gtl1450.tooltip.bioware_processor")
            adddark_greentier("gtl1450.tooltip.circuit_zpm_plain")
    }
})
