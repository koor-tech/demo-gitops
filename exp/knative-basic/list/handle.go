package function

import (
	"context"
	"fmt"
	"net/http"
	"os"
)

const FILES_DIR = "/files"

// Handle an HTTP Request.
func Handle(ctx context.Context, res http.ResponseWriter, req *http.Request) {
	fmt.Println("Reading directory")
	files, err := os.ReadDir(FILES_DIR)
	if err != nil {
		res.WriteHeader(http.StatusInternalServerError)
		fmt.Println(err)
		fmt.Fprint(res, "Error reading files directory")
		return
	}
	fmt.Printf("Found %d files\n", len(files))

	fmt.Fprintf(res, "Found %d files\n", len(files))
	for _, entry := range files {
		fmt.Fprintln(res, "-", entry.Name())
	}
}
