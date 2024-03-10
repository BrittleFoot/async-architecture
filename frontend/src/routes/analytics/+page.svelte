<script lang="ts">
	import { AnalyticsService, type Day, type DayInfo } from '$lib/api/analytics.js';
	import DaysAnalyticsWidget from '$lib/components/DaysAnalyticsWidget.svelte';
	import DaysPopugsWidget from '$lib/components/DaysPopugsWidget.svelte';
	import Skeleton from '$lib/components/Skeleton.svelte';
	import { onMount } from 'svelte';

	export let data;


    const analytics = new AnalyticsService(data.tokenInfo.accessToken);

    let dayPromise = Promise.resolve<Day[]>([]);
    let performerPromise = Promise.resolve<DayInfo[]>([]);

    onMount(() => {
        dayPromise = analytics.getDayAnalytics();
        performerPromise = analytics.getPerformersAnalytics();
    });

</script>

<h1>Analytics</h1>


{#await dayPromise}
    <Skeleton width="100%" height="16em" primaryColor="#1a202ccc" secondaryColor="#FFFFFF33"/>
{:then days}
    <DaysAnalyticsWidget {days}/>
{:catch error}
    <p>{error.message}</p>
{/await}

<p></p>

{#await performerPromise}
    <Skeleton width="100%" height="16em" primaryColor="#1a202ccc" secondaryColor="#FFFFFF33"/>
{:then days}
    <DaysPopugsWidget {days}/>
{:catch error}
    <p>{error.message}</p>
{/await}
