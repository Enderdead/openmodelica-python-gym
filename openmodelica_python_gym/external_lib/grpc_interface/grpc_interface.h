#ifndef GRPC_INTERFACE_LIBRARY_H
#define GRPC_INTERFACE_LIBRARY_H
extern "C" {
void grpcInterface(double t, double x[], int size_x, const char* in_label[], int size_in_label, const char* out_label[], int size_out_label, double sampling_rate);

double grpcGetter(double t, int index);
}
#endif //GRPC_INTERFACE_LIBRARY_H
