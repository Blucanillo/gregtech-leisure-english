ForgeEvents.onEvent("net.minecraftforge.event.entity.player.ItemTooltipEvent", event => {
    if (!LDLib.isClient()) return
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
            event.getToolTip().add(Component.literal("\u00a77" + tier_line(suprachronal.toUpperCase())))
        }
    })
    tiers.slice(0, 12).forEach((magneto_resonatic) => {
        if (event.getItemStack().getId() == "kubejs:circuit_resonatic_" + magneto_resonatic) {
            addtooltip("\u00a7d" + magneto_resonatic.toUpperCase() + text("gtl1450.tooltip.circuit_suffix"))
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
