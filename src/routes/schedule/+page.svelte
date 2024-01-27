<script lang="ts">
  import { onMount } from "svelte";
  import { writable, type Writable } from "svelte/store";
  import type { PageData } from "./$types";
  import { AccordionItem, Accordion, Button } from "flowbite-svelte";
  import { 
    QuestionCircleOutline,
    FileCodeOutline,
    FileVideoOutline,
    NewspapperOutline,
   } from 'flowbite-svelte-icons';
  import type { Schedule } from "$lib/util/helpme";

  export let courseID: string;
    export let courseName: string;

  export let data: PageData;

  const { schedule } = data;

  const scheduleStore: Writable<Schedule> = writable({
    titleMessage: "",
    lecturesPerDay: {},
  });

  onMount(async () => {
    try {
      const scheduleData = await data.schedule;
      scheduleStore.set(scheduleData); // Set the data in the store
    } catch (error) {
      console.error("Error loading schedule:", error);
    }
  });

  const convertSecondsToMinutesString = (seconds: number) => {
    const minutes = Math.floor(seconds / 60);
    const secondsLeft = seconds % 60;
    return `${minutes}m:${secondsLeft}s`;
  };

  /*
    
interface Schedule {
    titleMessage: string;
    lecturesPerDay: Record<string, { lectures: Lecture[], done: boolean }>;
}
*/

  const open_all = () => {
    Object.keys($scheduleStore.lecturesPerDay).forEach((day) => {
        $scheduleStore.lecturesPerDay[day].done = true;
    });
  };

  const close_all = () => {
    Object.keys($scheduleStore.lecturesPerDay).forEach((day) => {
        $scheduleStore.lecturesPerDay[day].done = false;
    });
  };
</script>

<div>
  {#await $scheduleStore}
    <p>Getting results...</p>
  {:then schedule}
  <div class="min-w-screen flex items-center justify-center flex-col px-5 py-5">
    <h1>
      {schedule.titleMessage}
    </h1>

    <section class="pt-4 px-4 flex flex-col items-center">
      <div class="button-container">
        <Button on:click={open_all}>Open all</Button>
        <Button on:click={close_all}>Close all</Button>
      </div>

      <Accordion multiple class="w-full py-4">
        {#each Object.keys(schedule.lecturesPerDay) as day (day)}
          <AccordionItem
            bind:open={$scheduleStore.lecturesPerDay[day].done}
            class="bg-gray-800 hover:bg-gray-700 w-full text-left overflow-hidden lg:min-w-[500px]"
          >
            <span slot="header" class="text-yellow-100 font-bold">{day}</span>
            {#each schedule.lecturesPerDay[day].lectures as lecture (lecture)}
              <div class="lecture-item text-black">
                <p
                >
                  {lecture.title} - {convertSecondsToMinutesString(
                    lecture.durationSeconds
                    
                  )}
                   ({lecture.type})
                </p>
              </div>
            {/each}
          </AccordionItem>
        {/each}
      </Accordion>
    </section>
    </div>
  {:catch error}
    <p>Something went wrong: {error.message}</p>
  {/await}
</div>
