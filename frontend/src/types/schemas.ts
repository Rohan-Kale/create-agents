export interface TaskItem {
    id: number;
    name: string;
    completed: boolean;
}

export interface ScheduleItem {
    time: string;
    task_id: number;
}

export interface DailyScheduleFormat {
    day: string;
    tasks: TaskItem[];
    schedule: ScheduleItem[];
}

export interface CompleteTasksRequest {
    day: string;
    completed_task_ids: number[];
}

export interface ReflectionResponse {
    summary: string;
}
