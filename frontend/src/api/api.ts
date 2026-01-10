import {
    DailyScheduleFormat,
    CompleteTasksRequest,
    ReflectionResponse,
} from '../types/schemas';


const BASE_URL = 'http://localhost:8000';

export async function draftSchedule(tasks: string[], day: string) {
    const res = await fetch(`$(BASE_URL)/draft`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ tasks, day } ),
    });
    return res.json();
}

export async function confirmSchedule(schedule: DailyScheduleFormat) {
    const res = await fetch(`$(BASE_URL)/confirm`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ schedule }),
    });
    if (!res.ok) {
        throw new Error('Failed to confirm schedule');
    }
    return res.json();
}

export async function getSchedule(day: string): Promise<DailyScheduleFormat> {
    const res = await fetch(`${BASE_URL}/schedule/${day}`);
    if (!res.ok) {
        throw new Error(`Failed to get schedule for day: ${day}`);
    }
    if (res.status === 404) {
        throw new Error(`No schedule found for day: ${day}`);
    }
    return res.json();
}

export async function completeTasks(day: string, completed_task_ids: number[]): Promise<DailyScheduleFormat> {
    const res = await fetch(`${BASE_URL}/complete/${day}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ completed_task_ids }),
    });
    if (!res.ok) {
        throw new Error(`Failed to complete tasks for day: ${day}`);
    }
    return res.json();
}

export async function reflect(day: string): Promise<ReflectionResponse> {
    const res = await fetch(`${BASE_URL}/reflect/${day}`, {
        method: 'POST',
    });
    if (!res.ok) {
        throw new Error(`Failed to get reflection for day: ${day}`);
    }
    return res.json();
}
