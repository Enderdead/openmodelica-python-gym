#ifndef GRPC_INTERFACE_LIBRARY_H
#define GRPC_INTERFACE_LIBRARY_H
extern "C" {
void grpcInterface(double x[], int size_x, const char* in_label[], int size_in_label, const char* out_label[], int size_out_label, double y[], int size_y);
}
#endif //GRPC_INTERFACE_LIBRARY_H