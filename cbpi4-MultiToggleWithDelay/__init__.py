import asyncio

from cbpi.api import CBPiStep, Property, parameters
from cbpi.api.timer import Timer



@parameters([
    Property.Actor(label="Actor01", description="Actor 01 toggled during this step"),
    Property.Select(label="toggle_type01", options=["On", "Off"], description="Toggle for Actor01"),
    Property.Number(label="Timer01", description="Delay after Actor01 (seconds)", configurable=True),

    Property.Actor(label="Actor02", description="Actor 02 toggled during this step"),
    Property.Select(label="toggle_type02", options=["On", "Off"], description="Toggle for Actor02"),
    Property.Number(label="Timer02", description="Delay after Actor02 (seconds)", configurable=True),

    Property.Actor(label="Actor03", description="Actor 03 toggled during this step"),
    Property.Select(label="toggle_type03", options=["On", "Off"], description="Toggle for Actor03"),
    Property.Number(label="Timer03", description="Delay after Actor03 (seconds)", configurable=True),

    Property.Actor(label="Actor04", description="Actor 04 toggled during this step"),
    Property.Select(label="toggle_type04", options=["On", "Off"], description="Toggle for Actor04"),
    Property.Number(label="Timer04", description="Delay after Actor04 (seconds)", configurable=True),

    Property.Actor(label="Actor05", description="Actor 05 toggled during this step"),
    Property.Select(label="toggle_type05", options=["On", "Off"], description="Toggle for Actor05"),
    Property.Number(label="Timer05", description="Delay after Actor05 (seconds)", configurable=True),

    Property.Actor(label="Actor06", description="Actor 06 toggled during this step"),
    Property.Select(label="toggle_type06", options=["On", "Off"], description="Toggle for Actor06"),
    Property.Number(label="Timer06", description="Delay after Actor06 (seconds)", configurable=True),

    Property.Actor(label="Actor07", description="Actor 07 toggled during this step"),
    Property.Select(label="toggle_type07", options=["On", "Off"], description="Toggle for Actor07"),
    Property.Number(label="Timer07", description="Delay after Actor07 (seconds)", configurable=True),

    Property.Actor(label="Actor08", description="Actor 08 toggled during this step"),
    Property.Select(label="toggle_type08", options=["On", "Off"], description="Toggle for Actor08"),
    Property.Number(label="Timer08", description="Delay after Actor08 (seconds)", configurable=True),

    Property.Actor(label="Actor09", description="Actor 09 toggled during this step"),
    Property.Select(label="toggle_type09", options=["On", "Off"], description="Toggle for Actor09"),
    Property.Number(label="Timer09", description="Delay after Actor09 (seconds)", configurable=True),

    Property.Actor(label="Actor10", description="Actor 10 toggled during this step"),
    Property.Select(label="toggle_type10", options=["On", "Off"], description="Toggle for Actor10"),
    Property.Number(label="Timer10", description="Delay after Actor10 (seconds)", configurable=True),
])
class MultiToggleWithDelay(CBPiStep):
    """
    Step that chains up to 10 actors with individual delays:
    Actor01 -> delay -> Actor02 -> delay -> ... -> Actor10 -> delay -> next step
    """

    async def on_timer_done(self, timer):
        self.phase_index += 1
        await self._run_phase()

    async def on_timer_update(self, timer, seconds):
        self.summary = Timer.format_time(seconds)
        await self.push_update()

    async def on_start(self):
        props = self.props
        self.actors = []
        self.toggles = []
        self.delays = []

        # Load actor, toggle and delay for each index 1–10
        for i in range(1, 11):
            actor = getattr(props, f"Actor{i:02}", None)
            toggle = getattr(props, f"toggle_type{i:02}", "Off")
            delay_val = getattr(props, f"Timer{i:02}", 0)

            try:
                delay = int(delay_val) if delay_val is not None else 0
            except:
                delay = 0

            self.actors.append(actor)
            self.toggles.append(toggle)
            self.delays.append(delay)

        # Nothing configured → skip
        if not any(a is not None or d > 0 for a, d in zip(self.actors, self.delays)):
            await self.next()
            return

        self.phase_index = 0
        self.timer = None
        await self._run_phase()

    async def _run_phase(self):
        if self.phase_index >= len(self.actors):
            self.summary = ""
            await self.next()
            return

        actor = self.actors[self.phase_index]
        toggle = self.toggles[self.phase_index]
        delay = self.delays[self.phase_index]

        # Fire actor
        if actor is not None:
            if toggle == "On":
                await self.actor_on(actor)
            else:
                await self.actor_off(actor)

        # Delay
        if delay > 0:
            self.timer = Timer(
                delay,
                on_update=self.on_timer_update,
                on_done=self.on_timer_done
            )
            self.timer.start()
        else:
            self.phase_index += 1
            await self._run_phase()

    async def on_stop(self):
        if getattr(self, "timer", None):
            await self.timer.stop()
        self.summary = ""
        await self.push_update()

    async def reset(self):
        self.timer = None
        self.phase_index = 0
        self.summary = ""

    async def run(self):
        while self.running:
            await asyncio.sleep(1)
        return StepResult.DONE


def setup(cbpi):
    cbpi.register_step(
        "Multi Toggle With Delay (10 Actors)",
        MultiToggleWithDelay
    )
