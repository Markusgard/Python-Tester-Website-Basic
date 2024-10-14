/**
 * Assignment 7
 */

/** album-info component should display songs and album cover **/
const albumInfoC = {
    props: ["albumId", "albumCover", "albumSongs", "timeTotal"],
    template: `
    <div id="album_info">
        <div id="album_cover">
        <img v-bind:src="albumCover" v-bind:alt="albumCover">
        </div>
        <div id="album_songs">
        <ol>
            <li v-for="song in albumSongs">{{ song[0] }}<span style="float:right">{{ song[1] }}</span></li>
            <br><span style="font-weight:bold">total duration</span><span style="float:right">{{ timeTotal }}</span>
        </ol>
        </div>
    </div>
    `,
}
