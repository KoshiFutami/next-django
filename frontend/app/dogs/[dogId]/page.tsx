import { getDog } from "@/lib/api/dogs";
import { Metadata } from "next";
import styles from "./page.module.css";
import Link from "next/link";

type PageProps = {
    params: Promise<{ dogId: string }>;
};

export async function generateMetadata({
    params,
}: PageProps): Promise<Metadata> {
    const { dogId } = await params;
    const dog = await getDog(dogId);
    return {
        title: `${dog.name} - Showcase`,
        description: `Showcase - ${dog.name}`,
    };
}

export default async function DogDetailPage({ params }: PageProps) {
    const { dogId } = await params;
    const dog = await getDog(dogId);

    return (
        <main className={styles.main}>
        <Link href="/" className={styles.back}>
          ← トップへ
        </Link>
        <article className={styles.card}>
          <h1 className={styles.title}>{dog.name}</h1>
          <dl className={styles.meta}>
            <dt>ID</dt>
            <dd>{dog.id}</dd>
            <dt>生年月日</dt>
            <dd>{dog.birth_date}</dd>
            <dt>体重</dt>
            <dd>{dog.weight}</dd>
            <dt>色</dt>
            <dd>{dog.color}</dd>
            <dt>性別</dt>
            <dd>{dog.gender}</dd>
            <dt>品種コード</dt>
            <dd>{dog.breed_code}</dd>
            <dt>プロフィール画像キー</dt>
            <dd>{dog.profile_image_key ?? "—"}</dd>
            <dt>登録日時</dt>
            <dd>{dog.created_at}</dd>
          </dl>
        </article>
      </main>
    )
}