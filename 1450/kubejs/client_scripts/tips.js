// priority: 99
// ---------------------------------------------------------------------------
// GTL1450 English localisation patch (KubeJS companion), revision 5
//
// The Chinese item tooltips that used to be hard-coded here are now translation
// keys, defined in assets/kubejs/lang/en_us.json and
// assets/minecraft/lang/en_us.json inside GTL1450-English-resourcepack.zip.
//
// Each key is resolved to its English *string* on the client and wrapped in
// Component.literal(...) exactly as the original script did, so the visible text
// -- including the leading § colour codes that the keys carry -- matches the
// original apart from the language.
//
// This file runs on the client at tooltip time, which is the only point where a
// lookup is safe: during StartupEvents the language table is still empty.
//
// Tooltip length, order and behaviour are unchanged.
// Install: drop this file over kubejs/client_scripts/tips.js in the instance
// (keep a backup).  Without the resource pack the keys are shown unresolved.
// ---------------------------------------------------------------------------

ItemEvents.tooltip(event => {
    function line(key) {
        // .string yields a wrapped Java String; the "" + coercion turns it into a real
        // JavaScript string before it reaches Component.literal.
        return Component.literal("" + Component.translatable(key).string)
    }

    event.add("kubejs:basic_control_circuit", line("gtl1450.tooltip.circuit_ulv"))
    event.add("kubejs:advanced_control_circuit", line("gtl1450.tooltip.circuit_lv"))
    event.add("kubejs:elite_control_circuit", line("gtl1450.tooltip.circuit_mv"))
    event.add("kubejs:ultimate_control_circuit", line("gtl1450.tooltip.circuit_hv"))
    event.add("kubejs:ultima_control_circuit", line("gtl1450.tooltip.circuit_ev"))
    event.add("kubejs:warped_ender_pearl", line("gtl1450.tooltip.warped_ender_pearl"))
    event.add("kubejs:hyper_stable_self_healing_adhesive", line("gtl1450.tooltip.self_healing_adhesive"))
    event.add("kubejs:black_body_naquadria_supersolid", line("gtl1450.tooltip.naquadria_supersolid"))
    event.add("kubejs:command_wand", line("gtl1450.tooltip.command_wand"))
    event.add("kubejs:uruium_coil_block", [line("gtl1450.tooltip.uruium_coil_temperature"), line("gtl1450.tooltip.uruium_coil_stellar")])
    event.add("kubejs:essence_block", line("gtl1450.tooltip.essence_block"))
    event.add("kubejs:draconium_block_charged", line("gtl1450.tooltip.draconium_block_charged"))
    event.add("minecraft:crimson_stem", line("gtl1450.tooltip.crimson_stem"))
    event.add("minecraft:warped_stem", line("gtl1450.tooltip.warped_stem"))
    event.add("minecraft:bone_block", line("gtl1450.tooltip.bone_block"))
    event.add("minecraft:moss_block", line("gtl1450.tooltip.moss_block"))
    event.add("minecraft:sculk", line("gtl1450.tooltip.sculk"))
    event.add("gtceu:magmatter_block", line("gtl1450.tooltip.magmatter_block"))
    event.add("minecraft:command_block", line("gtl1450.tooltip.command_block"))
    event.add("minecraft:chain_command_block", line("gtl1450.tooltip.chain_command_block"))
    event.add("minecraft:repeating_command_block", line("gtl1450.tooltip.repeating_command_block"))
    event.add("ad_astra:oxygen_loader", line("gtl1450.tooltip.oxygen_loader"))

    // Universal circuit boards: the original set this tooltip at registration time,
    // which cannot be translated (the language table is empty during startup).
    // The item name now comes from item.kubejs.<tier>_universal_circuit; this is
    // the tooltip half, resolved per display like every line above.
    const universal_circuit_tiers = ["ulv", "lv", "mv", "hv", "ev", "iv", "luv", "zpm", "uv", "uhv", "uev", "uiv", "uxv", "opv", "max"]
    universal_circuit_tiers.forEach((universal_circuit) => {
        event.add("kubejs:" + universal_circuit + "_universal_circuit", line("gtl1450.tooltip.universal_circuit_board.tip"))
    })
})
