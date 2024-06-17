import styles from "./page.module.css";
import { sql } from "@vercel/postgres";

export default async function Home() {
  const { rows } = await sql`SELECT * from news_links`;

  return (
    <main className={styles.main}>
      <table className={styles.table}>
        <thead>
          <tr>
            <td><h3>Headline</h3></td>
            <td><h3>Link</h3></td>
          </tr>
        </thead>
        <tbody>
          {rows.map((item) => (
            <tr key={0}>
              <td>{item.title}</td>
              <td><a href={item.url}>{item.url}</a></td>
            </tr>
          ))}
        </tbody>
      </table>
    </main>
  );
}
