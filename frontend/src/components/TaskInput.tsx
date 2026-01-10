import {useState} from "react";

interface Props {
    onSubmit: (tasks: string[]) => void;
}

export default function TaskInput({ onSubmit }: Props) {
    const [input, setInput] = useState("");

    const handleSubmit = () => {
        const tasks = input.split("\n").map((t) => t.trim()).filter(Boolean);

        onSubmit(tasks);
        setInput("");
    };

    return (
        <div>
            <h2>Enter today's Tasks</h2>
                <textarea
                    rows = {5}
                    value = {input}
                    onChange = {(e) => setInput(e.target.value)}
                    placeholder="One task per line"
                />
                <button onClick={handleSubmit}>Generate Schedule</button>
        </div>
    );
}


