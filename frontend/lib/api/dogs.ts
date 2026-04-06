import { getServerApiBaseUrl } from "./server-base-url";
import { apiPaths } from "./routes";
import { Dog, isDogJson } from "../types/dog";
import { notFound } from "next/navigation";


export async function fetchDog(id: string): Promise<Dog | null> {
    const baseUrl = getServerApiBaseUrl();
    const url = new URL(baseUrl + apiPaths.dogs.detail(id));
    const response = await fetch(url.toString());

    if (response.status === 404) {
        return null;
    }
    if (!response.ok) {
        throw new Error(`Failed to fetch dog: ${response.statusText}`);
    }

    const data = await response.json();
    if (!isDogJson(data)) {
        throw new Error('Invalid dog JSON');
    }
    return data;
}


export async function getDog(id: string): Promise<Dog> {
    const dog = await fetchDog(id);
    if (!dog) {
        notFound();
    }
    return dog;
}